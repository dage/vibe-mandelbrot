#!/usr/bin/env python3
# playloop.py - Automated vibe coding with DeepInfra vision and code models

import asyncio
import base64
import json
import subprocess
import time
import textwrap
import os
from pathlib import Path
from openai import OpenAI
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepinfra.com/v1/openai")
KEY = os.environ.get("OPENAI_API_KEY")
if not KEY:
    raise ValueError("OPENAI_API_KEY not found in environment. Please set it in your .env file.")

client = OpenAI(api_key=KEY, base_url=BASE)

VISION_MODEL = os.environ.get("VISION_MODEL", "meta-llama/Llama-3.2-90B-Vision-Instruct")
CODE_MODEL_QWEN = os.environ.get("CODE_MODEL_QWEN", "Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo")
CODE_MODEL_K2 = os.environ.get("CODE_MODEL_K2", "moonshotai/Kimi-K2-Instruct")

APP_URL = os.environ.get("APP_URL", "http://localhost:5173")
OUT = Path("ai_loop_artifacts")
OUT.mkdir(exist_ok=True)

VISION_SYSTEM = "You analyze web-app screenshots and console logs to find UX/visual/logic issues."
VISION_PROMPT = """You will receive one or more screenshots and recent console/network logs.
Return STRICT JSON with this schema:
{
  "issues": [
    {
      "title": "short",
      "severity": "low|med|high",
      "evidence": "what in the screenshot/logs proves it",
      "proposed_changes": [
        {"file": "relative/path", "change": "concise instruction describing exact edits"},
      ],
      "tests": [
        {"type":"unit|playwright", "name":"short", "spec":"what to assert"}
      ]
    }
  ],
  "notes": "optional"
}
Only JSON. Be concise. Prefer minimal viable fixes first.
"""

CODE_SYSTEM = "You are a senior code editor preparing a single instruction for Aider."
CODE_PROMPT = """Given this JSON of detected issues, produce ONE short instruction for Aider to apply.
Rules:
- List the files to modify at top as a bullet list.
- Then, numbered steps with precise edits.
- Include any new files to create.
- End with a short test plan (npm scripts).
Keep it compact and deterministic.
JSON from vision:

{vision_json}
"""

async def grab_screenshot_and_logs():
    ts = int(time.time())
    img_path = OUT / f"shot_{ts}.png"
    logs_path = OUT / f"logs_{ts}.txt"
    logs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Fix console logging
        def handle_console(msg):
            logs.append(f"[{msg.type}] {msg.text}")
        
        page.on("console", handle_console)
        
        try:
            await page.goto(APP_URL, wait_until="networkidle")
            await page.screenshot(path=str(img_path), full_page=True)
        finally:
            await browser.close()

    logs_path.write_text("\n".join(logs))
    return img_path, logs_path

def vision_analyze(img_path, logs_path):
    b64 = base64.b64encode(Path(img_path).read_bytes()).decode("utf-8")
    logs = Path(logs_path).read_text()[:20000]
    messages = [{
        "role": "system", "content": VISION_SYSTEM
    }, {
        "role": "user",
        "content": [
            {"type": "image_url",
             "image_url": {"url": f"data:image/png;base64,{b64}"}},
            {"type": "text",
             "text": VISION_PROMPT + "\n\nLogs:\n" + logs}
        ]
    }]
    resp = client.chat.completions.create(
        model=VISION_MODEL, messages=messages, temperature=0.2, max_tokens=1200
    )
    txt = resp.choices[0].message.content
    (OUT/"vision_raw.txt").write_text(txt)
    
    # Extract JSON from the response (handle extra text)
    import re
    json_match = re.search(r'\{.*\}', txt, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        return json.loads(json_str)
    else:
        # Fallback: try to parse the entire response
        return json.loads(txt)

def code_instruction(vision_json, model=CODE_MODEL_QWEN):
    prompt = CODE_PROMPT.format(vision_json=json.dumps(vision_json, ensure_ascii=False, indent=2))
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role":"system","content":CODE_SYSTEM},
                  {"role":"user","content":prompt}],
        temperature=0.1, max_tokens=2000
    )
    instr = resp.choices[0].message.content
    (OUT/"aider_message.txt").write_text(instr)
    return instr

def run_aider(instr, files=None, model=CODE_MODEL_QWEN):
    files = files or []
    cmd = [
        "aider",
        "--message", instr,
        "--model", model,
        "--auto-test"
    ] + files
    
    # Change to test-app directory if files are in that directory
    if files and any('test-app' in f for f in files):
        original_dir = os.getcwd()
        os.chdir('test-app')
        try:
            result = subprocess.call(cmd)
            return result
        finally:
            os.chdir(original_dir)
    else:
        return subprocess.call(cmd)

async def main():
    print("🎯 Starting vibe coding loop...")
    print(f"📸 Capturing screenshot from {APP_URL}")
    
    img, logs = await grab_screenshot_and_logs()
    print(f"✅ Screenshot saved: {img}")
    print(f"✅ Logs saved: {logs}")
    
    print("🔍 Analyzing with vision model...")
    vjson = vision_analyze(img, logs)
    print(f"✅ Vision analysis complete: {len(vjson.get('issues', []))} issues found")
    
    print("💻 Generating code instruction...")
    instr = code_instruction(vjson, model=CODE_MODEL_QWEN)
    print("✅ Code instruction generated")
    
    # Extract files from JSON to focus edits
    files = sorted({c.get("file","") for i in vjson.get("issues",[]) for c in i.get("proposed_changes",[]) if c.get("file")})
    if files:
        print(f"📁 Targeting files: {', '.join(files)}")
    
    print("🚀 Running Aider...")
    rc = run_aider(instr, files=files, model=CODE_MODEL_QWEN)
    print(f"✅ Aider exit code: {rc}")
    
    if rc == 0:
        print("🎉 Loop completed successfully!")
    else:
        print("⚠️  Aider encountered issues. Check logs.")

if __name__ == "__main__":
    asyncio.run(main()) 