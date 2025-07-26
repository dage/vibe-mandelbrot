#!/bin/bash
# setup_deepinfra.sh - Set up DeepInfra environment for vibe coding

echo "🚀 Setting up DeepInfra environment for vibe coding..."

# Check if API key is provided
if [ -z "$1" ]; then
    echo "❌ Please provide your DeepInfra API key as an argument"
    echo "Usage: ./setup_deepinfra.sh YOUR_API_KEY"
    echo ""
    echo "Get your API key from: https://deepinfra.com/"
    exit 1
fi

API_KEY="$1"

# Set environment variables
export OPENAI_API_KEY="$API_KEY"
export OPENAI_API_BASE="https://api.deepinfra.com/v1/openai"

echo "✅ Environment variables set:"
echo "   OPENAI_API_KEY: ${API_KEY:0:8}..."
echo "   OPENAI_API_BASE: $OPENAI_API_BASE"
echo ""

# Activate conda environment
echo "🔧 Activating vibes conda environment..."
conda activate vibes

if [ $? -eq 0 ]; then
    echo "✅ Vibes environment activated"
else
    echo "❌ Failed to activate vibes environment"
    exit 1
fi

# Verify dependencies
echo "🔍 Verifying dependencies..."
echo "   Python: $(python --version)"
echo "   Aider: $(aider --version)"
echo "   Playwright: $(python -c "import playwright; print('installed')" 2>/dev/null || echo 'not installed')"
echo "   OpenAI: $(python -c "import openai; print('installed')" 2>/dev/null || echo 'not installed')"
echo ""

# Test API connection
echo "🌐 Testing DeepInfra API connection..."
python -c "
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url=os.environ['OPENAI_API_BASE']
)

try:
    response = client.chat.completions.create(
        model='Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo',
        messages=[{'role': 'user', 'content': 'Hello'}],
        max_tokens=10
    )
    print('✅ API connection successful!')
except Exception as e:
    print(f'❌ API connection failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup complete! You're ready for vibe coding."
    echo ""
    echo "Next steps:"
    echo "1. Start your dev server: npm run dev"
    echo "2. Run the vibe loop: python playloop.py"
    echo ""
    echo "To make environment variables permanent, add to your shell profile:"
    echo "export OPENAI_API_KEY=\"$API_KEY\""
    echo "export OPENAI_API_BASE=\"https://api.deepinfra.com/v1/openai\""
else
    echo "❌ Setup failed. Please check your API key and try again."
    exit 1
fi 