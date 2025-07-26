#!/usr/bin/env python3
# demo_vibe_loop.py - Demo version of vibe coding loop

import asyncio
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright

APP_URL = "http://localhost:5173"
OUT = Path("ai_loop_artifacts")
OUT.mkdir(exist_ok=True)

# Mock vision analysis results
MOCK_VISION_RESULT = {
    "issues": [
        {
            "title": "Missing semicolons in JavaScript",
            "severity": "medium",
            "evidence": "JavaScript code has missing semicolons which can cause issues",
            "proposed_changes": [
                {"file": "test-app/main.js", "change": "Add missing semicolons to increment and decrement functions"}
            ],
            "tests": [
                {"type": "unit", "name": "Counter functions work", "spec": "Test that counter increments and decrements correctly"}
            ]
        },
        {
            "title": "Todo items lack delete functionality",
            "severity": "high",
            "evidence": "Todo list items cannot be deleted, making the app unusable",
            "proposed_changes": [
                {"file": "test-app/main.js", "change": "Add delete functionality to todo items"},
                {"file": "test-app/style.css", "change": "Add styling for delete buttons"}
            ],
            "tests": [
                {"type": "playwright", "name": "Todo delete works", "spec": "Test that todo items can be deleted"}
            ]
        },
        {
            "title": "Missing keyboard accessibility",
            "severity": "medium",
            "evidence": "App cannot be used with keyboard navigation",
            "proposed_changes": [
                {"file": "test-app/main.js", "change": "Add keyboard event listeners for accessibility"},
                {"file": "test-app/index.html", "change": "Add proper ARIA labels and focus management"}
            ],
            "tests": [
                {"type": "playwright", "name": "Keyboard navigation", "spec": "Test that all functions work with keyboard"}
            ]
        }
    ],
    "notes": "Demo analysis showing intentional issues in the test app"
}

# Mock code instruction
MOCK_CODE_INSTRUCTION = """Files to modify:
- test-app/main.js
- test-app/style.css
- test-app/index.html

1. Fix JavaScript syntax by adding missing semicolons in increment and decrement functions
2. Add delete functionality to todo items with click handlers
3. Add keyboard accessibility with proper event listeners
4. Add ARIA labels and focus management to HTML elements
5. Style delete buttons in CSS

Test plan:
- Test counter functionality
- Test todo add/delete functionality  
- Test keyboard navigation
- Test color changer functionality"""

async def grab_screenshot_and_logs():
    """Capture screenshot and logs from the running app"""
    ts = int(time.time())
    img_path = OUT / f"demo_shot_{ts}.png"
    logs_path = OUT / f"demo_logs_{ts}.txt"
    logs = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
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
    except Exception as e:
        print(f"⚠️  Screenshot capture failed: {e}")
        # Create mock files for demo
        img_path.write_text("Mock screenshot")
        logs_path.write_text("Mock console logs")
        return img_path, logs_path

def demo_vision_analyze(img_path, logs_path):
    """Mock vision analysis"""
    print(f"🔍 Analyzing screenshot: {img_path}")
    print(f"📝 Processing logs: {logs_path}")
    
    # Save mock vision result
    (OUT/"demo_vision_raw.txt").write_text(json.dumps(MOCK_VISION_RESULT, indent=2))
    
    return MOCK_VISION_RESULT

def demo_code_instruction(vision_json):
    """Mock code instruction generation"""
    print("💻 Generating code instruction from vision analysis...")
    
    # Save mock instruction
    (OUT/"demo_aider_message.txt").write_text(MOCK_CODE_INSTRUCTION)
    
    return MOCK_CODE_INSTRUCTION

def demo_run_aider(instr, files=None):
    """Mock Aider execution"""
    print("🚀 Simulating Aider execution...")
    print(f"📁 Files to modify: {files or 'all'}")
    print(f"📋 Instruction: {instr[:100]}...")
    
    # Simulate some processing time
    time.sleep(2)
    
    print("✅ Mock Aider completed successfully!")
    return 0

async def main():
    print("🎯 Starting DEMO vibe coding loop...")
    print(f"📸 Capturing screenshot from {APP_URL}")
    
    # Step 1: Capture screenshot and logs
    img, logs = await grab_screenshot_and_logs()
    print(f"✅ Screenshot saved: {img}")
    print(f"✅ Logs saved: {logs}")
    
    # Step 2: Vision analysis
    print("🔍 Analyzing with vision model...")
    vjson = demo_vision_analyze(img, logs)
    print(f"✅ Vision analysis complete: {len(vjson.get('issues', []))} issues found")
    
    # Step 3: Code instruction generation
    print("💻 Generating code instruction...")
    instr = demo_code_instruction(vjson)
    print("✅ Code instruction generated")
    
    # Step 4: Extract files to modify
    files = sorted({c.get("file","") for i in vjson.get("issues",[]) for c in i.get("proposed_changes",[]) if c.get("file")})
    if files:
        print(f"📁 Targeting files: {', '.join(files)}")
    
    # Step 5: Run Aider (mock)
    print("🚀 Running Aider...")
    rc = demo_run_aider(instr, files=files)
    print(f"✅ Aider exit code: {rc}")
    
    if rc == 0:
        print("🎉 Demo loop completed successfully!")
        print("\n📋 Summary of suggested improvements:")
        for issue in vjson.get("issues", []):
            print(f"  • {issue['title']} ({issue['severity']}): {issue['evidence']}")
    else:
        print("⚠️  Demo encountered issues.")

if __name__ == "__main__":
    asyncio.run(main()) 