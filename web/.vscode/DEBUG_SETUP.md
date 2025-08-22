# TKA Web App - Simplified Debugging Setup

## Quick Start (Recommended Workflow)

1. **Start the dev server manually:**

   ```bash
   npm run dev
   ```

   Wait for the server to start (you'll see "Local: http://localhost:5173")

2. **Start debugging:**
   - Press `F5` or click the "Debug TKA Web App" button in VS Code
   - The debugger will launch immediately (no waiting for pre-launch tasks)

3. **Set breakpoints and debug:**
   - Set breakpoints in your TypeScript/Svelte files
   - Breakpoints will trigger in VS Code's debugger (not browser console)
   - Use VS Code's debug panel for variables, call stack, etc.

## Alternative: Use VS Code Task

If you prefer, you can use the VS Code task to start the dev server:

- Press `Ctrl+Shift+P` → "Tasks: Run Task" → "Start TKA Dev Server"
- Then press `F5` to start debugging

## What Changed

- **Single configuration**: Only "Debug TKA Web App" (removed confusing alternatives)
- **No pre-launch delays**: Eliminated "waiting for pre-launch task" messages
- **Seamless breakpoints**: TypeScript/Svelte breakpoints work directly in VS Code
- **Simplified workflow**: Start dev server → Click debug → Breakpoints work

## Troubleshooting

- **Breakpoints not working?** Make sure the dev server is running on port 5173
- **Source maps issues?** The vite.config.ts is already optimized for debugging
- **Chrome not launching?** The debugger uses a dedicated Chrome profile in `.vscode/chrome-debug-profile`
