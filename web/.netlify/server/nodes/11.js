import * as universal from '../entries/pages/motion-tester/_page.ts.js';
import * as server from '../entries/pages/motion-tester/_page.server.ts.js';

export const index = 11;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/motion-tester/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/motion-tester/+page.ts";
export { server };
export const server_id = "src/routes/motion-tester/+page.server.ts";
export const imports = ["_app/immutable/nodes/11.tPG0xt5R.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/j-n_PhSD.js","_app/immutable/chunks/DvtHUlSU.js","_app/immutable/chunks/bWGpElgn.js","_app/immutable/chunks/zHtQjFda.js","_app/immutable/chunks/B6HM2C-u.js","_app/immutable/chunks/BOSm_y1M.js","_app/immutable/chunks/DZNFex5L.js","_app/immutable/chunks/C0KUShqx.js","_app/immutable/chunks/CLPY3JhS.js","_app/immutable/chunks/DK2gEQ8N.js","_app/immutable/chunks/Brsx3ROp.js","_app/immutable/chunks/Dp1pzeXC.js","_app/immutable/chunks/C21CGrb7.js","_app/immutable/chunks/BS9O6h9z.js"];
export const stylesheets = ["_app/immutable/assets/AboutTab.XL5PghD6.css","_app/immutable/assets/MainApplication.DNYK2yJx.css"];
export const fonts = [];
