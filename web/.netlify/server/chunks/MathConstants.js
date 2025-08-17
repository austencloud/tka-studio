var Location = /* @__PURE__ */ ((Location2) => {
  Location2["NORTH"] = "n";
  Location2["EAST"] = "e";
  Location2["SOUTH"] = "s";
  Location2["WEST"] = "w";
  Location2["NORTHEAST"] = "ne";
  Location2["SOUTHEAST"] = "se";
  Location2["SOUTHWEST"] = "sw";
  Location2["NORTHWEST"] = "nw";
  return Location2;
})(Location || {});
const PI = Math.PI;
const HALF_PI = PI / 2;
({
  [Location.EAST]: 0,
  [Location.SOUTH]: HALF_PI,
  [Location.WEST]: PI,
  [Location.NORTH]: -HALF_PI,
  [Location.NORTHEAST]: -HALF_PI / 2,
  [Location.SOUTHEAST]: HALF_PI / 2,
  [Location.SOUTHWEST]: PI + HALF_PI / 2,
  [Location.NORTHWEST]: PI - HALF_PI / 2
});
