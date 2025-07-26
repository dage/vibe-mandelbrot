# Vibe Mandelbrot - AI-Powered Coding with DeepInfra

This project sets up an automated coding environment using Aider, DeepInfra's vision and code models, and Playwright for screenshot analysis.

## What is Vite?

Vite is a modern build tool and development server that provides:
- **Lightning fast** development with instant hot module replacement
- **Zero config** setup with sensible defaults
- **Rich features** including TypeScript, JSX, and CSS support
- **Optimized builds** for production

## Setup Instructions

### 1. Environment Setup

1. Copy the environment template:
   ```bash
   cp env_template.txt .env
   ```

2. Edit `.env` and replace `YOUR_API_KEY_HERE` with your actual DeepInfra API key:
   ```bash
   # Get your API key from: https://deepinfra.com/
   OPENAI_API_KEY=your_actual_api_key_here
   ```

### 2. Activate Environment

```bash
# Activate the vibes conda environment
conda activate vibes

# Or use the setup script
./setup_env.sh
```

### 3. Create a Web App (Optional)

If you don't have a web app yet, you can create a simple Vite app:

```bash
# Create a new Vite project in a subdirectory
npm create vite@latest my-app -- --template vanilla
cd my-app
npm install
npm run dev
```

### 4. Run the Vibe Coding Loop

#### Demo Mode (No API Key Required)
```bash
# Run the demo to see how the system works
./run_demo.sh
```

#### Full Mode (Requires API Key)
1. Start your development server (if using Vite):
   ```bash
   npm run dev
   ```

2. Run the automated coding loop:
   ```bash
   python playloop.py
   # or
   ./run_vibe_test.sh
   ```

## How It Works

1. **Screenshot Capture**: Playwright takes a screenshot of your running app
2. **Vision Analysis**: Llama-3.2-90B-Vision analyzes the screenshot and console logs
3. **Issue Detection**: Identifies UX/UI/logic issues and proposes changes
4. **Code Generation**: Qwen3-Coder generates specific code instructions
5. **Auto-Apply**: Aider applies the changes automatically with testing

## Models Used

- **Vision**: `meta-llama/Llama-3.2-90B-Vision-Instruct` - Analyzes screenshots
- **Code**: `Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo` - Generates code changes
- **Alternative**: `moonshotai/Kimi-K2-Instruct` - Text-only code generation

## Files

- `playloop.py` - Main automation script
- `demo_vibe_loop.py` - Demo version (no API required)
- `run_demo.sh` - Demo runner script
- `run_vibe_test.sh` - Full vibe loop runner
- `setup_env.sh` - Environment activation helper
- `setup_deepinfra.sh` - DeepInfra API setup (alternative)
- `env_template.txt` - Environment variables template
- `test_setup.py` - Environment testing script
- `ai_loop_artifacts/` - Generated screenshots and analysis files

## Tips

- Start with manual runs before setting up automatic loops
- The system captures full-page screenshots and console logs
- Changes are applied with automatic testing and linting
- You can switch between Qwen3-Coder and Kimi K2 models easily

## Troubleshooting

### API Connection Issues
- Make sure your API key is valid and has sufficient credits
- Check your internet connection
- Try running the demo first: `./run_demo.sh`

### App Not Starting
- Ensure your dev server is running on the expected port (default: 5173)
- Check that all dependencies are installed: `python test_setup.py`

### Debugging
- Check the `ai_loop_artifacts/` directory for screenshots and analysis files
- Run `python test_setup.py` to verify your environment
- Use the demo mode to test the workflow without API calls 