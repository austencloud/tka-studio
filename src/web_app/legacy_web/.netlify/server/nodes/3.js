import * as server from '../entries/pages/auth/callback/_platform_/_page.server.ts.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/auth/callback/_platform_/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/auth/callback/[platform]/+page.server.ts";
export const imports = ["_app/immutable/nodes/3.DGZeYGm9.js","_app/immutable/chunks/DHwDQIkX.js","_app/immutable/chunks/CycfVVW7.js"];
export const stylesheets = ["_app/immutable/assets/3.CmiNdA8G.css"];
export const fonts = [];
