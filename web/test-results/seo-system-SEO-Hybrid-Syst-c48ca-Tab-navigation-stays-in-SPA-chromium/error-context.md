# Page snapshot

```yaml
- text: "[plugin:vite:import-analysis] Failed to resolve import \"./components/settings/SettingsDialog.svelte\" from \"src/lib/shared/MainApplication.svelte\". Does the file exist? 22 | } from \"./state/app-state.svelte\"; 23 | 24 | import SettingsDialog from \"./components/settings/SettingsDialog.svelte\"; | ^ 25 | import ErrorScreen from \"./foundation/ui/ErrorScreen.svelte\"; 26 | import LoadingScreen from \"./foundation/ui/LoadingScreen.svelte\"; at TransformPluginContext._formatLog (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42499:41) at TransformPluginContext.error (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42496:16) at normalizeUrl (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40475:23) at process.processTicksAndRejections (node:internal/process/task_queues:105:5) at async file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40594:37 at async Promise.all (index 5) at async TransformPluginContext.transform (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40521:7) at async EnvironmentPluginContainer.transform (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42294:18) at async loadAndTransform (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:35735:27) at async viteTransformMiddleware (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:37250:24 Click outside, press Esc key, or fix the code to dismiss. You can also disable this overlay by setting"
- code: server.hmr.overlay
- text: to
- code: "false"
- text: in
- code: vite.config.ts
- text: .
```