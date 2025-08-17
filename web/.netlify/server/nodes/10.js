import * as universal from '../entries/pages/metadata-tester/_page.ts.js';
import * as server from '../entries/pages/metadata-tester/_page.server.ts.js';

export const index = 10;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/metadata-tester/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/metadata-tester/+page.ts";
export { server };
export const server_id = "src/routes/metadata-tester/+page.server.ts";
export const imports = ["_app/immutable/nodes/10.DlmbnPKl.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/j-n_PhSD.js","_app/immutable/chunks/DvtHUlSU.js","_app/immutable/chunks/zHtQjFda.js","_app/immutable/chunks/BOSm_y1M.js","_app/immutable/chunks/CLPY3JhS.js","_app/immutable/chunks/DK2gEQ8N.js","_app/immutable/chunks/C0KUShqx.js"];
export const stylesheets = ["_app/immutable/assets/10.Pblfeowh.css"];
export const fonts = [];
