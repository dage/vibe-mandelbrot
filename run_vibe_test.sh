#!/bin/bash
# run_vibe_test.sh - Start test app and run vibe coding loop

echo "🚀 Starting Vibe Coding Test..."

# Activate conda environment
echo "🔧 Activating vibes environment..."
conda activate vibes

# Check if test app exists
if [ ! -d "test-app" ]; then
    echo "❌ test-app directory not found!"
    exit 1
fi

# Start the test app in the background
echo "🌐 Starting test app..."
cd test-app
npm run dev &
DEV_PID=$!
cd ..

# Wait for the app to start
echo "⏳ Waiting for app to start..."
sleep 5

# Check if app is running
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ Test app is running at http://localhost:5173"
else
    echo "❌ Test app failed to start"
    kill $DEV_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎯 Running vibe coding loop..."
echo "The AI will analyze the app and suggest improvements."
echo "Press Ctrl+C to stop the loop."
echo ""

# Run the vibe loop
python playloop.py

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $DEV_PID 2>/dev/null
echo "✅ Done!" 