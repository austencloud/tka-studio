# Page snapshot

```yaml
- text: "[plugin:vite:import-analysis] Failed to resolve import \"./hooks\" from \"src/lib/shared/pictograph/components/Pictograph.svelte\". Does the file exist? 6 | import { onMount } from \"svelte\"; 7 | import PictographSvg from \"./PictographSvg.svelte\"; 8 | import { useArrowPositioning, useComponentLoading, usePictographData } from \"./hooks\"; | ^ 9 | 10 | var root = $.add_locations($.from_html(`<div><!></div>`), Pictograph[$.FILENAME], [[73, 0]]); at TransformPluginContext._formatLog (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42499:41) at TransformPluginContext.error (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42496:16) at normalizeUrl (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40475:23) at process.processTicksAndRejections (node:internal/process/task_queues:105:5) at async file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40594:37 at async Promise.all (index 4) at async TransformPluginContext.transform (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40521:7) at async EnvironmentPluginContainer.transform (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42294:18) at async loadAndTransform (file:///C:/TKA/web/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:35735:27 Click outside, press Esc key, or fix the code to dismiss. You can also disable this overlay by setting"
- code: server.hmr.overlay
- text: to
- code: "false"
- text: in
- code: vite.config.ts
- text: .
```