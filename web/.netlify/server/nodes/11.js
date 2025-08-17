import * as universal from '../entries/pages/motion-tester/_page.ts.js';
import * as server from '../entries/pages/motion-tester/_page.server.ts.js';

export const index = 11;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/motion-tester/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/motion-tester/+page.ts";
export { server };
export const server_id = "src/routes/motion-tester/+page.server.ts";
export const imports = ["_app/immutable/nodes/11.fAqr0l66.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/BtI6aIiM.js","_app/immutable/chunks/IUYm_0rb.js","_app/immutable/chunks/B5I7GX32.js","_app/immutable/chunks/DVUHJB5u.js","_app/immutable/chunks/DA8cGw4Q.js","_app/immutable/chunks/C-eppkXD.js","_app/immutable/chunks/CuI29WU7.js","_app/immutable/chunks/C0KUShqx.js","_app/immutable/chunks/C8ay5gD4.js","_app/immutable/chunks/C-ElHC__.js","_app/immutable/chunks/DAUS0jAM.js","_app/immutable/chunks/Dp1pzeXC.js","_app/immutable/chunks/BE__5pEg.js","_app/immutable/chunks/Q46znR_b.js"];
export const stylesheets = ["_app/immutable/assets/AboutTab.XL5PghD6.css","_app/immutable/assets/MainApplication.COGOMJ_4.css"];
export const fonts = [];
