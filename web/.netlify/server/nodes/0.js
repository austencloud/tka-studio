import * as server from '../entries/pages/_layout.server.ts.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { server };
export const server_id = "src/routes/+layout.server.ts";
export const imports = ["_app/immutable/nodes/0.DXes1xPE.js","_app/immutable/chunks/Dp1pzeXC.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/B7NnFPNL.js","_app/immutable/chunks/1IXZttPU.js","_app/immutable/chunks/BFCtTEbx.js"];
export const stylesheets = ["_app/immutable/assets/0.CK2s6s0l.css"];
export const fonts = [];
