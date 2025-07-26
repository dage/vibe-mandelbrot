#!/usr/bin/env python3
# test_setup.py - Test the vibe coding environment setup

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are properly set"""
    print("🔍 Testing environment setup...")
    
    # Load .env file
    load_dotenv()
    
    # Check required environment variables
    required_vars = ["OPENAI_API_KEY", "OPENAI_API_BASE"]
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {value[:20]}..." if len(value) > 20 else f"✅ {var}: {value}")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please copy env_template.txt to .env and add your API key")
        return False
    
    return True

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n🔍 Testing dependencies...")
    
    dependencies = [
        ("openai", "OpenAI SDK"),
        ("playwright", "Playwright"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing_deps = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} not found")
            missing_deps.append(module)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Run: conda activate vibes && pip install " + " ".join(missing_deps))
        return False
    
    return True

def test_aider():
    """Test if aider is available"""
    print("\n🔍 Testing Aider...")
    
    try:
        import subprocess
        result = subprocess.run(["aider", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Aider: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Aider failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Aider not found: {e}")
        return False

def test_api_connection():
    """Test DeepInfra API connection"""
    print("\n🌐 Testing DeepInfra API connection...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_API_BASE"]
        )
        
        response = client.chat.completions.create(
            model="Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo",
            messages=[{"role": "user", "content": "Say 'Hello from DeepInfra!'"}],
            max_tokens=10
        )
        
        print(f"✅ API connection successful!")
        print(f"   Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def main():
    print("🚀 Vibe Coding Environment Test")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_dependencies,
        test_aider,
        test_api_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! You're ready for vibe coding.")
        print("\nNext steps:")
        print("1. Start your dev server: npm run dev")
        print("2. Run the vibe loop: python playloop.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 