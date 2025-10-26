# Page snapshot

```yaml
- text: "[plugin:vite:import-analysis] Failed to resolve import \"../../construct\" from \"src/lib/modules/build/shared/components/ConstructTabContent.svelte\". Does the file exist? 5 | import * as $ from 'svelte/internal/client'; 6 | import { fade } from \"svelte/transition\"; 7 | import { OptionViewer, StartPositionPicker } from \"../../construct\"; | ^ 8 | 9 | var root_1 = $.add_locations($.from_html(`<div class=\"picker-transition-wrapper s-ehw0yDqvy_q7\"><!></div>`), ConstructTabContent[$.FILENAME], [[35, 8]]); at TransformPluginContext._formatLog (file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42499:41) at TransformPluginContext.error (file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42496:16) at normalizeUrl (file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40475:23) at process.processTicksAndRejections (node:internal/process/task_queues:105:5) at async file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40594:37 at async Promise.all (index 3) at async TransformPluginContext.transform (file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:40521:7) at async EnvironmentPluginContainer.transform (file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:42294:18) at async loadAndTransform (file:///f:/_THE%20KINETIC%20ALPHABET/_TKA%20APP/node_modules/vite/dist/node/chunks/dep-DBxKXgDP.js:35735:27 Click outside, press Esc key, or fix the code to dismiss. You can also disable this overlay by setting"
- code: server.hmr.overlay
- text: to
- code: "false"
- text: in
- code: vite.config.ts
- text: .
```