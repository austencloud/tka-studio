import * as server from '../entries/pages/_layout.server.ts.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { server };
export const server_id = "src/routes/+layout.server.ts";
export const imports = ["_app/immutable/nodes/0.Bo9zdgZF.js","_app/immutable/chunks/Dp1pzeXC.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/B5I7GX32.js","_app/immutable/chunks/IUYm_0rb.js","_app/immutable/chunks/C-eppkXD.js"];
export const stylesheets = ["_app/immutable/assets/0.D_yQlDLH.css"];
export const fonts = [];
