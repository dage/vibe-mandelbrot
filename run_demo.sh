#!/bin/bash
# run_demo.sh - Start test app and run demo vibe loop

echo "🚀 Starting Vibe Coding Demo..."

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
echo "🎯 Running demo vibe coding loop..."
echo "This demonstrates how the AI analyzes the app and suggests improvements."
echo ""

# Run the demo
python demo_vibe_loop.py

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $DEV_PID 2>/dev/null
echo "✅ Demo completed!" 