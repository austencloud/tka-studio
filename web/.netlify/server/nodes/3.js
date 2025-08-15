import * as universal from '../entries/pages/about/_page.ts.js';
import * as server from '../entries/pages/about/_page.server.ts.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/about/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/about/+page.ts";
export { server };
export const server_id = "src/routes/about/+page.server.ts";
export const imports = ["_app/immutable/nodes/3.6XAxIyoZ.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/B7NnFPNL.js","_app/immutable/chunks/1IXZttPU.js","_app/immutable/chunks/Dhmuwhcn.js","_app/immutable/chunks/B_FYZ0MZ.js","_app/immutable/chunks/BMPWZhgT.js","_app/immutable/chunks/DEbdyNju.js","_app/immutable/chunks/BFCtTEbx.js","_app/immutable/chunks/7C95ztYV.js"];
export const stylesheets = ["_app/immutable/assets/AboutTab.BzlsHyU4.css"];
export const fonts = [];
