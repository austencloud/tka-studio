import * as universal from '../entries/pages/arrow-debug/_page.ts.js';
import * as server from '../entries/pages/arrow-debug/_page.server.ts.js';

export const index = 4;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/arrow-debug/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/arrow-debug/+page.ts";
export { server };
export const server_id = "src/routes/arrow-debug/+page.server.ts";
export const imports = ["_app/immutable/nodes/4.D_rreRcH.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/BtI6aIiM.js","_app/immutable/chunks/IUYm_0rb.js","_app/immutable/chunks/B5I7GX32.js","_app/immutable/chunks/C-eppkXD.js","_app/immutable/chunks/DVUHJB5u.js","_app/immutable/chunks/C8ay5gD4.js","_app/immutable/chunks/DAUS0jAM.js","_app/immutable/chunks/C-ElHC__.js","_app/immutable/chunks/CuI29WU7.js","_app/immutable/chunks/C0KUShqx.js"];
export const stylesheets = ["_app/immutable/assets/4._AKWQ0TY.css"];
export const fonts = [];
