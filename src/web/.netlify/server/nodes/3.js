export const index = 3;
let component_cache;
export const component = async () =>
  (component_cache ??= (
    await import("../entries/pages/constructor/_page.svelte.js")
  ).default);
export const imports = [
  "_app/immutable/nodes/3.BhY9txdJ.js",
  "_app/immutable/chunks/Bzak7iHL.js",
  "_app/immutable/chunks/CoBlTT59.js",
  "_app/immutable/chunks/DN5_AtCC.js",
  "_app/immutable/chunks/C6DgC_sk.js",
  "_app/immutable/chunks/BB2Cxm-G.js",
  "_app/immutable/chunks/BmW-jtJn.js",
  "_app/immutable/chunks/Dp1pzeXC.js",
  "_app/immutable/chunks/mzEfG4fk.js",
  "_app/immutable/chunks/2O9R1QKD.js",
  "_app/immutable/chunks/BSjZHGnr.js",
  "_app/immutable/chunks/CPuNEIat.js",
];
export const stylesheets = [
  "_app/immutable/assets/MainApplication.LDUzbgf5.css",
];
export const fonts = [];
