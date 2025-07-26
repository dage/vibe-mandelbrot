#!/bin/bash
# setup_env.sh - Activate vibes conda environment and verify setup

echo "Activating vibes conda environment..."
conda activate vibes

if [ $? -eq 0 ]; then
    echo "✅ Vibes environment activated successfully"
    echo "Python version: $(python --version)"
    echo "Aider version: $(aider --version)"
    echo ""
    echo "You can now use aider and other tools in this environment."
    echo "To deactivate, run: conda deactivate"
else
    echo "❌ Failed to activate vibes environment"
    echo "Make sure the environment exists: conda env list"
fi 