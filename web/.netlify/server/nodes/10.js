import * as universal from '../entries/pages/metadata-tester/_page.ts.js';
import * as server from '../entries/pages/metadata-tester/_page.server.ts.js';

export const index = 10;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/metadata-tester/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/metadata-tester/+page.ts";
export { server };
export const server_id = "src/routes/metadata-tester/+page.server.ts";
export const imports = ["_app/immutable/nodes/10.B6VCO0m-.js","_app/immutable/chunks/Bzak7iHL.js","_app/immutable/chunks/BtI6aIiM.js","_app/immutable/chunks/IUYm_0rb.js","_app/immutable/chunks/DVUHJB5u.js","_app/immutable/chunks/C-eppkXD.js","_app/immutable/chunks/C8ay5gD4.js","_app/immutable/chunks/C-ElHC__.js","_app/immutable/chunks/C0KUShqx.js"];
export const stylesheets = ["_app/immutable/assets/10.Pblfeowh.css"];
export const fonts = [];
