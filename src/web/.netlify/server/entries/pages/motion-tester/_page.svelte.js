import { b as attr, c as attr_class, p as pop, a as push, d as ensure_array_like, e as escape_html, m as maybe_selected, h as head } from "../../../chunks/index.js";
import "clsx";
const PI = Math.PI;
const TWO_PI = 2 * PI;
const HALF_PI = PI / 2;
const locationAngles = {
  e: 0,
  s: HALF_PI,
  w: PI,
  n: -HALF_PI
};
function normalizeAnglePositive(angle) {
  let norm = angle % TWO_PI;
  return norm < 0 ? norm + TWO_PI : norm;
}
function normalizeAngleSigned(angle) {
  let norm = normalizeAnglePositive(angle);
  return norm > PI ? norm - TWO_PI : norm;
}
function mapPositionToAngle(loc) {
  const l = loc?.toLowerCase();
  return locationAngles[l] ?? 0;
}
function mapOrientationToAngle(ori, centerPathAngle) {
  if (!ori) return centerPathAngle + PI;
  const l = ori.toLowerCase();
  if (locationAngles.hasOwnProperty(l)) {
    return locationAngles[l];
  }
  if (l === "in") {
    return normalizeAnglePositive(centerPathAngle + PI);
  }
  if (l === "out") {
    return normalizeAnglePositive(centerPathAngle);
  }
  return normalizeAnglePositive(centerPathAngle + PI);
}
function lerpAngle(a, b, t) {
  const d = normalizeAngleSigned(b - a);
  return normalizeAnglePositive(a + d * t);
}
function calculateProIsolationStaffAngle(centerPathAngle, _propRotDir) {
  return normalizeAnglePositive(centerPathAngle + PI);
}
function calculateProTargetAngle(startCenterAngle, targetCenterAngle, startStaffAngle, turns, propRotDir) {
  console.log(
    "🔧 [PRO DEBUG] ===== CALCULATING PRO TARGET ANGLE WITH TURNS ====="
  );
  console.log("🔧 [PRO DEBUG] Input parameters:");
  console.log(
    "🔧 [PRO DEBUG]   startCenterAngle:",
    startCenterAngle,
    "radians",
    (startCenterAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   targetCenterAngle:",
    targetCenterAngle,
    "radians",
    (targetCenterAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   startStaffAngle:",
    startStaffAngle,
    "radians",
    (startStaffAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [PRO DEBUG]   turns:", turns);
  console.log("🔧 [PRO DEBUG]   propRotDir:", propRotDir);
  let delta = normalizeAngleSigned(targetCenterAngle - startCenterAngle);
  const base = delta;
  const turn = PI * turns;
  const dir = propRotDir?.toLowerCase() === "ccw" ? -1 : 1;
  const result = normalizeAnglePositive(startStaffAngle + base + turn * dir);
  console.log("🔧 [PRO DEBUG] Calculation steps:");
  console.log(
    "🔧 [PRO DEBUG]   delta (target - start):",
    delta,
    "radians",
    (delta * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   base (delta):",
    base,
    "radians",
    (base * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [PRO DEBUG]   turn (PI * turns):",
    turn,
    "radians",
    (turn * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [PRO DEBUG]   dir (rotation direction):", dir);
  console.log(
    "🔧 [PRO DEBUG]   raw result (start + base + turn * dir):",
    startStaffAngle + base + turn * dir
  );
  console.log(
    "🔧 [PRO DEBUG]   normalized result:",
    result,
    "radians",
    (result * 180 / PI).toFixed(1),
    "degrees"
  );
  return result;
}
function calculateAntispinTargetAngle(startCenterAngle, targetCenterAngle, startStaffAngle, turns, propRotDir) {
  console.log("🔧 [ANTI DEBUG] ===== CALCULATING ANTI-SPIN TARGET ANGLE =====");
  console.log("🔧 [ANTI DEBUG] Input parameters:");
  console.log(
    "🔧 [ANTI DEBUG]   startCenterAngle:",
    startCenterAngle,
    "radians",
    (startCenterAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   targetCenterAngle:",
    targetCenterAngle,
    "radians",
    (targetCenterAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   startStaffAngle:",
    startStaffAngle,
    "radians",
    (startStaffAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [ANTI DEBUG]   turns:", turns);
  console.log("🔧 [ANTI DEBUG]   propRotDir:", propRotDir);
  let delta = normalizeAngleSigned(targetCenterAngle - startCenterAngle);
  const base = -delta;
  const turn = PI * turns;
  const dir = propRotDir?.toLowerCase() === "ccw" ? -1 : 1;
  const result = normalizeAnglePositive(startStaffAngle + base + turn * dir);
  console.log("🔧 [ANTI DEBUG] Calculation steps:");
  console.log(
    "🔧 [ANTI DEBUG]   delta (target - start):",
    delta,
    "radians",
    (delta * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   base (-delta):",
    base,
    "radians",
    (base * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log(
    "🔧 [ANTI DEBUG]   turn (PI * turns):",
    turn,
    "radians",
    (turn * 180 / PI).toFixed(1),
    "degrees"
  );
  console.log("🔧 [ANTI DEBUG]   dir (rotation direction):", dir);
  console.log(
    "🔧 [ANTI DEBUG]   raw result (start + base + turn * dir):",
    startStaffAngle + base + turn * dir
  );
  console.log(
    "🔧 [ANTI DEBUG]   normalized result:",
    result,
    "radians",
    (result * 180 / PI).toFixed(1),
    "degrees"
  );
  return result;
}
function calculateDashTargetAngle(startStaffAngle, endOri, targetCenterAngle) {
  if (endOri?.toLowerCase() === "in") {
    return normalizeAnglePositive(targetCenterAngle + PI);
  } else if (endOri?.toLowerCase() === "out") {
    return targetCenterAngle;
  }
  return startStaffAngle;
}
function calculateStepEndpoints(stepDefinition, propType) {
  const attributes = stepDefinition.blue_attributes;
  if (!attributes) return null;
  const {
    start_loc,
    end_loc,
    start_ori,
    end_ori,
    motion_type,
    prop_rot_dir,
    turns = 0
  } = attributes;
  const startCenterAngle = mapPositionToAngle(start_loc);
  const startStaffAngle = mapOrientationToAngle(
    start_ori || "in",
    startCenterAngle
  );
  const targetCenterAngle = mapPositionToAngle(end_loc);
  let calculatedTargetStaffAngle;
  console.log("🔧 [ENDPOINT DEBUG] ===== CALCULATING STEP ENDPOINTS =====");
  console.log("🔧 [ENDPOINT DEBUG] Motion type:", motion_type);
  console.log("🔧 [ENDPOINT DEBUG] Prop type:", propType);
  console.log("🔧 [ENDPOINT DEBUG] Motion attributes:", {
    start_loc,
    end_loc,
    start_ori,
    end_ori,
    motion_type,
    prop_rot_dir,
    turns
  });
  switch (motion_type) {
    case "pro":
      console.log("🔧 [ENDPOINT DEBUG] Processing PRO motion");
      if (turns > 0) {
        console.log("🔧 [ENDPOINT DEBUG] PRO motion with turns:", turns);
        calculatedTargetStaffAngle = calculateProTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          turns,
          prop_rot_dir || "cw"
        );
      } else {
        console.log("🔧 [ENDPOINT DEBUG] PRO motion isolation (zero turns)");
        calculatedTargetStaffAngle = calculateProIsolationStaffAngle(
          targetCenterAngle
        );
      }
      break;
    case "anti":
      console.log("🔧 [ENDPOINT DEBUG] Processing ANTI motion");
      calculatedTargetStaffAngle = calculateAntispinTargetAngle(
        startCenterAngle,
        targetCenterAngle,
        startStaffAngle,
        turns || 0,
        prop_rot_dir || "cw"
      );
      break;
    case "static":
      console.log("🔧 [ENDPOINT DEBUG] Processing STATIC motion");
      const endOriAngleStatic = mapOrientationToAngle(
        end_ori || "in",
        targetCenterAngle
      );
      const angleDiffStatic = normalizeAngleSigned(
        endOriAngleStatic - startStaffAngle
      );
      calculatedTargetStaffAngle = Math.abs(angleDiffStatic) > 0.1 ? endOriAngleStatic : startStaffAngle;
      break;
    case "dash":
      console.log("🔧 [ENDPOINT DEBUG] Processing DASH motion");
      calculatedTargetStaffAngle = calculateDashTargetAngle(
        startStaffAngle,
        end_ori || "in",
        targetCenterAngle
      );
      break;
    default:
      console.warn(`Unknown motion type '${motion_type}'. Treating as static.`);
      calculatedTargetStaffAngle = startStaffAngle;
      break;
  }
  console.log(
    "🔧 [ENDPOINT DEBUG] Calculated target staff angle:",
    calculatedTargetStaffAngle,
    "radians",
    (calculatedTargetStaffAngle * 180 / PI).toFixed(1),
    "degrees"
  );
  if (motion_type !== "pro") {
    const endOriAngleOverride = mapOrientationToAngle(
      end_ori || "in",
      targetCenterAngle
    );
    const explicitEndOri = ["n", "e", "s", "w", "in", "out"].includes(
      (end_ori || "").toLowerCase()
    );
    if (explicitEndOri) {
      calculatedTargetStaffAngle = endOriAngleOverride;
    }
  }
  return {
    startCenterAngle,
    startStaffAngle,
    targetCenterAngle,
    targetStaffAngle: calculatedTargetStaffAngle
  };
}
function MotionTesterCanvas($$payload, $$props) {
  push();
  let { state } = $$props;
  const CANVAS_SIZE = 500;
  $$payload.out.push(`<div class="canvas-container svelte-h8wi5s"><h2 class="svelte-h8wi5s">🎬 Motion Visualization</h2> <canvas${attr("width", CANVAS_SIZE)}${attr("height", CANVAS_SIZE)} class="motion-canvas svelte-h8wi5s"></canvas> <div class="animation-controls svelte-h8wi5s"><button${attr_class("control-btn svelte-h8wi5s", void 0, { "active": state.animationState.isPlaying })}${attr("disabled", state.animationState.isPlaying, true)}>▶ Play</button> <button class="control-btn svelte-h8wi5s"${attr("disabled", !state.animationState.isPlaying, true)}>⏸ Pause</button> <button class="control-btn svelte-h8wi5s">⏹ Reset</button> <button class="control-btn svelte-h8wi5s"${attr("disabled", state.animationState.isPlaying, true)}>⏭ Step</button></div> <div class="motion-legend svelte-h8wi5s"><div class="legend-item svelte-h8wi5s"><div class="legend-color start svelte-h8wi5s"></div> <span>Start Position</span></div> <div class="legend-item svelte-h8wi5s"><div class="legend-color current svelte-h8wi5s"></div> <span>Current Position</span></div> <div class="legend-item svelte-h8wi5s"><div class="legend-color end svelte-h8wi5s"></div> <span>End Position</span></div> <div class="legend-item svelte-h8wi5s"><div class="legend-color path svelte-h8wi5s"></div> <span>Motion Path</span></div></div></div>`);
  pop();
}
function MotionParameterPanel($$payload, $$props) {
  push();
  let { state } = $$props;
  const locationGrid = [[null, "n", null], ["w", "center", "e"], [null, "s", null]];
  const each_array = ensure_array_like(locationGrid);
  const each_array_2 = ensure_array_like(locationGrid);
  $$payload.out.push(`<div class="motion-params-panel svelte-1vo3bjc"><h2 class="svelte-1vo3bjc">🎯 Motion Parameters</h2> <div class="input-group svelte-1vo3bjc"><label class="svelte-1vo3bjc">Start Location</label> <div class="location-grid svelte-1vo3bjc"><!--[-->`);
  for (let $$index_1 = 0, $$length = each_array.length; $$index_1 < $$length; $$index_1++) {
    let row = each_array[$$index_1];
    const each_array_1 = ensure_array_like(row);
    $$payload.out.push(`<div class="location-row svelte-1vo3bjc"><!--[-->`);
    for (let $$index = 0, $$length2 = each_array_1.length; $$index < $$length2; $$index++) {
      let location = each_array_1[$$index];
      if (location) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<button${attr_class("location-btn svelte-1vo3bjc", void 0, { "active": state.motionParams.startLoc === location })}>${escape_html(location === "center" ? "⊙" : location.toUpperCase())}</button>`);
      } else {
        $$payload.out.push("<!--[!-->");
        $$payload.out.push(`<div class="location-spacer svelte-1vo3bjc"></div>`);
      }
      $$payload.out.push(`<!--]-->`);
    }
    $$payload.out.push(`<!--]--></div>`);
  }
  $$payload.out.push(`<!--]--></div></div> <div class="input-group svelte-1vo3bjc"><label class="svelte-1vo3bjc">End Location</label> <div class="location-grid svelte-1vo3bjc"><!--[-->`);
  for (let $$index_3 = 0, $$length = each_array_2.length; $$index_3 < $$length; $$index_3++) {
    let row = each_array_2[$$index_3];
    const each_array_3 = ensure_array_like(row);
    $$payload.out.push(`<div class="location-row svelte-1vo3bjc"><!--[-->`);
    for (let $$index_2 = 0, $$length2 = each_array_3.length; $$index_2 < $$length2; $$index_2++) {
      let location = each_array_3[$$index_2];
      if (location) {
        $$payload.out.push("<!--[-->");
        $$payload.out.push(`<button${attr_class("location-btn svelte-1vo3bjc", void 0, { "active": state.motionParams.endLoc === location })}>${escape_html(location === "center" ? "⊙" : location.toUpperCase())}</button>`);
      } else {
        $$payload.out.push("<!--[!-->");
        $$payload.out.push(`<div class="location-spacer svelte-1vo3bjc"></div>`);
      }
      $$payload.out.push(`<!--]-->`);
    }
    $$payload.out.push(`<!--]--></div>`);
  }
  $$payload.out.push(`<!--]--></div></div> <div class="input-group svelte-1vo3bjc"><label for="motionType" class="svelte-1vo3bjc">Motion Type</label> <select id="motionType" class="svelte-1vo3bjc">`);
  $$payload.select_value = state.motionParams.motionType;
  $$payload.out.push(`<option value="pro"${maybe_selected($$payload, "pro")} class="svelte-1vo3bjc">Pro</option><option value="anti"${maybe_selected($$payload, "anti")} class="svelte-1vo3bjc">Anti</option><option value="static"${maybe_selected($$payload, "static")} class="svelte-1vo3bjc">Static</option><option value="dash"${maybe_selected($$payload, "dash")} class="svelte-1vo3bjc">Dash</option><option value="fl"${maybe_selected($$payload, "fl")} class="svelte-1vo3bjc">Float</option><option value="none"${maybe_selected($$payload, "none")} class="svelte-1vo3bjc">None</option>`);
  $$payload.select_value = void 0;
  $$payload.out.push(`</select></div> <div class="input-group svelte-1vo3bjc"><label for="turns" class="svelte-1vo3bjc">Turns</label> <input id="turns" type="number" min="0" max="10" step="0.5"${attr("value", state.motionParams.turns)} class="svelte-1vo3bjc"/></div> <div class="input-group svelte-1vo3bjc"><label for="propRotDir" class="svelte-1vo3bjc">Rotation Direction</label> <select id="propRotDir" class="svelte-1vo3bjc">`);
  $$payload.select_value = state.motionParams.propRotDir;
  $$payload.out.push(`<option value="cw"${maybe_selected($$payload, "cw")} class="svelte-1vo3bjc">Clockwise (CW)</option><option value="ccw"${maybe_selected($$payload, "ccw")} class="svelte-1vo3bjc">Counter-Clockwise (CCW)</option><option value="no_rot"${maybe_selected($$payload, "no_rot")} class="svelte-1vo3bjc">No Rotation</option>`);
  $$payload.select_value = void 0;
  $$payload.out.push(`</select></div> <div class="input-group svelte-1vo3bjc"><label for="startOri" class="svelte-1vo3bjc">Start Orientation</label> <select id="startOri" class="svelte-1vo3bjc">`);
  $$payload.select_value = state.motionParams.startOri;
  $$payload.out.push(`<option value="in"${maybe_selected($$payload, "in")} class="svelte-1vo3bjc">In</option><option value="out"${maybe_selected($$payload, "out")} class="svelte-1vo3bjc">Out</option><option value="n"${maybe_selected($$payload, "n")} class="svelte-1vo3bjc">North</option><option value="e"${maybe_selected($$payload, "e")} class="svelte-1vo3bjc">East</option><option value="s"${maybe_selected($$payload, "s")} class="svelte-1vo3bjc">South</option><option value="w"${maybe_selected($$payload, "w")} class="svelte-1vo3bjc">West</option><option value="clock"${maybe_selected($$payload, "clock")} class="svelte-1vo3bjc">Clock</option><option value="counter"${maybe_selected($$payload, "counter")} class="svelte-1vo3bjc">Counter</option>`);
  $$payload.select_value = void 0;
  $$payload.out.push(`</select></div> <div class="input-group svelte-1vo3bjc"><label for="endOri" class="svelte-1vo3bjc">End Orientation</label> <select id="endOri" class="svelte-1vo3bjc">`);
  $$payload.select_value = state.motionParams.endOri;
  $$payload.out.push(`<option value="in"${maybe_selected($$payload, "in")} class="svelte-1vo3bjc">In</option><option value="out"${maybe_selected($$payload, "out")} class="svelte-1vo3bjc">Out</option><option value="n"${maybe_selected($$payload, "n")} class="svelte-1vo3bjc">North</option><option value="e"${maybe_selected($$payload, "e")} class="svelte-1vo3bjc">East</option><option value="s"${maybe_selected($$payload, "s")} class="svelte-1vo3bjc">South</option><option value="w"${maybe_selected($$payload, "w")} class="svelte-1vo3bjc">West</option><option value="clock"${maybe_selected($$payload, "clock")} class="svelte-1vo3bjc">Clock</option><option value="counter"${maybe_selected($$payload, "counter")} class="svelte-1vo3bjc">Counter</option>`);
  $$payload.select_value = void 0;
  $$payload.out.push(`</select></div> <div class="motion-info svelte-1vo3bjc"><h3 class="svelte-1vo3bjc">Current Motion</h3> <div class="motion-description svelte-1vo3bjc">${escape_html(state.motionDescription)}</div></div> <div class="input-group svelte-1vo3bjc"><label for="progressSlider" class="svelte-1vo3bjc">Animation Progress</label> <div class="slider-container svelte-1vo3bjc"><input id="progressSlider" type="range" min="0" max="100"${attr("value", state.animationState.progress * 100)} class="svelte-1vo3bjc"/> <div class="slider-value svelte-1vo3bjc">${escape_html((state.animationState.progress * 100).toFixed(1))}%</div></div></div> <div class="input-group svelte-1vo3bjc"><label for="speedSlider" class="svelte-1vo3bjc">Animation Speed</label> <div class="slider-container svelte-1vo3bjc"><input id="speedSlider" type="range" min="1" max="100"${attr("value", state.animationState.speed * 1e3)} class="svelte-1vo3bjc"/> <div class="slider-value svelte-1vo3bjc">${escape_html((state.animationState.speed * 1e3).toFixed(0))}%</div></div></div> <div class="orientation-visualizer svelte-1vo3bjc"><div class="orientation-display svelte-1vo3bjc"><h4 class="svelte-1vo3bjc">Start Orientation</h4> <div class="orientation-arrow svelte-1vo3bjc">${escape_html(state.getOrientationArrow(state.motionParams.startOri))}</div> <div class="orientation-text svelte-1vo3bjc">${escape_html(state.motionParams.startOri)}</div></div> <div class="orientation-display svelte-1vo3bjc"><h4 class="svelte-1vo3bjc">End Orientation</h4> <div class="orientation-arrow svelte-1vo3bjc">${escape_html(state.getOrientationArrow(state.motionParams.endOri))}</div> <div class="orientation-text svelte-1vo3bjc">${escape_html(state.motionParams.endOri)}</div></div></div></div>`);
  pop();
}
function DebugInfoPanel($$payload, $$props) {
  push();
  let { state } = $$props;
  function radToDeg(rad) {
    return (rad * 180 / Math.PI).toFixed(1);
  }
  function formatAngle(rad) {
    return rad.toFixed(3);
  }
  $$payload.out.push(`<div class="debug-panel svelte-1ehcr87"><h2 class="svelte-1ehcr87">🔧 Debug Information</h2> <div class="debug-section current-state svelte-1ehcr87"><h3 class="svelte-1ehcr87">Current Prop State</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Center Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.currentPropState.centerAngle))} rad</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Staff Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.currentPropState.staffAngle))} rad</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">X Position:</span> <span class="value svelte-1ehcr87">${escape_html(state.currentPropState.x.toFixed(1))} px</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Y Position:</span> <span class="value svelte-1ehcr87">${escape_html(state.currentPropState.y.toFixed(1))} px</span></div></div> `);
  if (state.debugInfo && state.endpoints) {
    $$payload.out.push("<!--[-->");
    $$payload.out.push(`<div class="debug-section svelte-1ehcr87"><h3 class="svelte-1ehcr87">Start Endpoints</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Center Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.debugInfo.startCenterAngle))} rad</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Staff Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.debugInfo.startStaffAngle))} rad</span></div></div> <div class="debug-section svelte-1ehcr87"><h3 class="svelte-1ehcr87">Target Endpoints</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Center Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.debugInfo.targetCenterAngle))} rad</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Staff Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.debugInfo.targetStaffAngle))} rad</span></div></div> <div class="debug-section svelte-1ehcr87"><h3 class="svelte-1ehcr87">Motion Calculation</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Motion Type:</span> <span class="value svelte-1ehcr87">${escape_html(state.motionParams.motionType)}</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Delta Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.debugInfo.deltaAngle))} rad</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Turn Angle:</span> <span class="value svelte-1ehcr87">${escape_html(formatAngle(state.debugInfo.turnAngle))} rad</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Interpolation (t):</span> <span class="value svelte-1ehcr87">${escape_html(state.debugInfo.interpolationT.toFixed(3))}</span></div></div> <div class="debug-section svelte-1ehcr87"><h3 class="svelte-1ehcr87">Grid Positions</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Start Location:</span> <span class="value svelte-1ehcr87">${escape_html(state.motionParams.startLoc)}</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">End Location:</span> <span class="value svelte-1ehcr87">${escape_html(state.motionParams.endLoc)}</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Distance:</span> <span class="value svelte-1ehcr87">${escape_html(state.debugInfo.distance.toFixed(1))}°</span></div></div> <div class="debug-section svelte-1ehcr87"><h3 class="svelte-1ehcr87">Angle Conversions</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Center (degrees):</span> <span class="value svelte-1ehcr87">${escape_html(radToDeg(state.currentPropState.centerAngle))}°</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Staff (degrees):</span> <span class="value svelte-1ehcr87">${escape_html(radToDeg(state.currentPropState.staffAngle))}°</span></div></div>`);
  } else {
    $$payload.out.push("<!--[!-->");
  }
  $$payload.out.push(`<!--]--> <div class="debug-section summary svelte-1ehcr87"><h3 class="svelte-1ehcr87">Motion Summary</h3> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Description:</span> <span class="value motion-desc svelte-1ehcr87">${escape_html(state.motionDescription)}</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Progress:</span> <span class="value svelte-1ehcr87">${escape_html((state.animationState.progress * 100).toFixed(1))}%</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Speed:</span> <span class="value svelte-1ehcr87">${escape_html((state.animationState.speed * 1e3).toFixed(0))}%</span></div> <div class="debug-item svelte-1ehcr87"><span class="label svelte-1ehcr87">Playing:</span> <span${attr_class("value svelte-1ehcr87", void 0, { "playing": state.animationState.isPlaying })}>${escape_html(state.animationState.isPlaying ? "Yes" : "No")}</span></div></div> <div class="debug-section svelte-1ehcr87"><h3 class="svelte-1ehcr87">Quick Tests</h3> <div class="quick-test-grid svelte-1ehcr87"><button class="quick-test-btn svelte-1ehcr87">N→E Pro</button> <button class="quick-test-btn svelte-1ehcr87">N→S Anti 1T</button> <button class="quick-test-btn svelte-1ehcr87">E→W Pro 2T</button> <button class="quick-test-btn svelte-1ehcr87">S→N Static</button></div></div></div>`);
  pop();
}
const GRID_VIEWBOX_SIZE = 950;
const GRID_CENTER = GRID_VIEWBOX_SIZE / 2;
const GRID_HALFWAY_POINT_OFFSET = 151.5;
function createMotionTesterState() {
  let motionParams = {
    startLoc: "n",
    endLoc: "e",
    motionType: "pro",
    turns: 0,
    propRotDir: "cw",
    startOri: "in",
    endOri: "in"
  };
  let animationState = { progress: 0, isPlaying: false, speed: 0.01 };
  let endpoints = () => {
    const stepDef = { blue_attributes: motionParams };
    return calculateStepEndpoints(stepDef, "blue");
  };
  let currentPropState = () => {
    if (!endpoints) {
      return { centerAngle: 0, staffAngle: 0, x: 0, y: 0 };
    }
    const t = animationState.progress;
    const centerAngle = lerpAngle(endpoints.startCenterAngle, endpoints.targetCenterAngle, t);
    const staffAngle = lerpAngle(endpoints.startStaffAngle, endpoints.targetStaffAngle, t);
    const radius = GRID_HALFWAY_POINT_OFFSET;
    const centerX = GRID_CENTER;
    const centerY = GRID_CENTER;
    const x = centerX + Math.cos(centerAngle) * radius;
    const y = centerY + Math.sin(centerAngle) * radius;
    return { centerAngle, staffAngle, x, y };
  };
  let motionDescription = () => {
    return `${motionParams.startLoc.toUpperCase()} → ${motionParams.endLoc.toUpperCase()} (${motionParams.motionType}, ${motionParams.turns} turns, ${motionParams.propRotDir.toUpperCase()})`;
  };
  let animationFrameId = null;
  function startAnimation() {
    animationState.isPlaying = true;
    animate();
  }
  function pauseAnimation() {
    animationState.isPlaying = false;
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
  }
  function resetAnimation() {
    pauseAnimation();
    animationState.progress = 0;
  }
  function stepAnimation() {
    animationState.progress = Math.min(1, animationState.progress + 0.1);
  }
  function animate() {
    if (!animationState.isPlaying) return;
    animationState.progress += animationState.speed;
    if (animationState.progress > 1) {
      animationState.progress = 0;
    }
    animationFrameId = requestAnimationFrame(animate);
  }
  function updateMotionParam(key, value) {
    motionParams[key] = value;
  }
  function setProgress(progress) {
    animationState.progress = Math.max(0, Math.min(1, progress));
  }
  function setSpeed(speed) {
    animationState.speed = Math.max(1e-3, Math.min(0.1, speed));
  }
  function setStartLocation(location) {
    updateMotionParam("startLoc", location);
  }
  function setEndLocation(location) {
    updateMotionParam("endLoc", location);
  }
  let debugInfo = () => {
    if (!endpoints) return null;
    const deltaAngle = normalizeAngleSigned(endpoints.targetCenterAngle - endpoints.startCenterAngle);
    const turnAngle = Math.PI * motionParams.turns;
    const distance = Math.abs(deltaAngle) * 180 / Math.PI;
    return {
      startCenterAngle: endpoints.startCenterAngle,
      startStaffAngle: endpoints.startStaffAngle,
      targetCenterAngle: endpoints.targetCenterAngle,
      targetStaffAngle: endpoints.targetStaffAngle,
      deltaAngle,
      turnAngle,
      distance,
      interpolationT: animationState.progress
    };
  };
  function getOrientationArrow(orientation) {
    const arrows = {
      "in": "→",
      "out": "←",
      "n": "↑",
      "e": "→",
      "s": "↓",
      "w": "←",
      "clock": "↻",
      "counter": "↺"
    };
    return arrows[orientation] || "→";
  }
  function destroy() {
    pauseAnimation();
  }
  return {
    // Reactive state (getters)
    get motionParams() {
      return motionParams;
    },
    get animationState() {
      return animationState;
    },
    get endpoints() {
      return endpoints;
    },
    get currentPropState() {
      return currentPropState;
    },
    get motionDescription() {
      return motionDescription;
    },
    get debugInfo() {
      return debugInfo;
    },
    // Actions
    updateMotionParam,
    setProgress,
    setSpeed,
    setStartLocation,
    setEndLocation,
    startAnimation,
    pauseAnimation,
    resetAnimation,
    stepAnimation,
    getOrientationArrow,
    destroy
  };
}
function _page($$payload, $$props) {
  push();
  const state = createMotionTesterState();
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>TKA Motion Tester - Individual Motion Testing</title>`;
  });
  $$payload.out.push(`<div class="motion-tester-container svelte-5og8ed"><header class="tester-header svelte-5og8ed"><h1 class="svelte-5og8ed">🎯 TKA Motion Tester</h1> <p class="svelte-5og8ed">Test individual motion sequences with visual feedback and debugging</p></header> <main class="tester-main svelte-5og8ed"><div class="panel motion-params svelte-5og8ed">`);
  MotionParameterPanel($$payload, { state });
  $$payload.out.push(`<!----></div> <div class="panel canvas-panel svelte-5og8ed">`);
  MotionTesterCanvas($$payload, { state });
  $$payload.out.push(`<!----></div> <div class="panel debug-panel svelte-5og8ed">`);
  DebugInfoPanel($$payload, { state });
  $$payload.out.push(`<!----></div></main></div>`);
  pop();
}
export {
  _page as default
};
