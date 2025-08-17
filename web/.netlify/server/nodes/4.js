import * as universal from '../entries/pages/arrow-debug/_page.ts.js';
import * as server from '../entries/pages/arrow-debug/_page.server.ts.js';

export const index = 4;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/arrow-debug/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/arrow-debug/+page.ts";
export { server };
export const server_id = "src/routes/arrow-debug/+page.server.ts";
export const imports = ["_app/immutable/nodes/4.MFbxLNwA.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/j-n_PhSD.js","_app/immutable/chunks/DvtHUlSU.js","_app/immutable/chunks/bWGpElgn.js","_app/immutable/chunks/BOSm_y1M.js","_app/immutable/chunks/zHtQjFda.js","_app/immutable/chunks/CLPY3JhS.js","_app/immutable/chunks/Brsx3ROp.js","_app/immutable/chunks/DK2gEQ8N.js","_app/immutable/chunks/DZNFex5L.js","_app/immutable/chunks/C0KUShqx.js"];
export const stylesheets = ["_app/immutable/assets/4._AKWQ0TY.css"];
export const fonts = [];
