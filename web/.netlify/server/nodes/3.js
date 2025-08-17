import * as universal from '../entries/pages/about/_page.ts.js';
import * as server from '../entries/pages/about/_page.server.ts.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/about/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/about/+page.ts";
export { server };
export const server_id = "src/routes/about/+page.server.ts";
export const imports = ["_app/immutable/nodes/3.CW0B2uUQ.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/bWGpElgn.js","_app/immutable/chunks/DvtHUlSU.js","_app/immutable/chunks/C21CGrb7.js","_app/immutable/chunks/CLPY3JhS.js","_app/immutable/chunks/DBndVoH3.js","_app/immutable/chunks/BS9O6h9z.js","_app/immutable/chunks/j-n_PhSD.js","_app/immutable/chunks/BOSm_y1M.js","_app/immutable/chunks/Brsx3ROp.js","_app/immutable/chunks/DK2gEQ8N.js"];
export const stylesheets = ["_app/immutable/assets/AboutTab.XL5PghD6.css"];
export const fonts = [];
