import * as universal from '../entries/pages/about/_page.ts.js';
import * as server from '../entries/pages/about/_page.server.ts.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/about/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/about/+page.ts";
export { server };
export const server_id = "src/routes/about/+page.server.ts";
export const imports = ["_app/immutable/nodes/3.DcTJWUSM.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/B5I7GX32.js","_app/immutable/chunks/IUYm_0rb.js","_app/immutable/chunks/BE__5pEg.js","_app/immutable/chunks/C8ay5gD4.js","_app/immutable/chunks/DBndVoH3.js","_app/immutable/chunks/Q46znR_b.js","_app/immutable/chunks/BtI6aIiM.js","_app/immutable/chunks/C-eppkXD.js","_app/immutable/chunks/DAUS0jAM.js","_app/immutable/chunks/C-ElHC__.js"];
export const stylesheets = ["_app/immutable/assets/AboutTab.XL5PghD6.css"];
export const fonts = [];
