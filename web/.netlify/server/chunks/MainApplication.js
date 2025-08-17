import { e as escape_html, d as attr_style, f as stringify, g as getContext, h as head, p as pop, a as push } from "./index.js";
import "./png-metadata-extractor.js";
import "./MathConstants.js";
import "clsx";
/* empty css                                       */
const initState = {
  initializationProgress: 0
};
function getInitializationProgress() {
  return initState.initializationProgress;
}
function LoadingScreen($$payload, $$props) {
  let { progress = 0, message = "Loading..." } = $$props;
  const clampedProgress = Math.max(0, Math.min(100, progress));
  $$payload.out.push(`<!---->/** * Loading Screen - Pure Svelte 5 implementation * * Shows loading progress
during application initialization. */ <div class="loading-screen svelte-u01yoh"><div class="loading-content svelte-u01yoh"><div class="spinner svelte-u01yoh"></div> <h2 class="svelte-u01yoh">TKA - The Kinetic Constructor</h2> <p class="message svelte-u01yoh">${escape_html(message)}</p> <div class="progress-container svelte-u01yoh"><div class="progress-bar svelte-u01yoh"><div class="progress-fill svelte-u01yoh"${attr_style(`width: ${stringify(clampedProgress)}%`)}></div></div> <span class="progress-text svelte-u01yoh">${escape_html(Math.round(clampedProgress))}%</span></div></div></div>`);
}
typeof window !== "undefined" && window.location.search.includes("debug=foldable");
function MainApplication($$payload, $$props) {
  push();
  getContext("di-container");
  let initializationProgress = getInitializationProgress();
  head($$payload, ($$payload2) => {
    $$payload2.title = `<title>TKA Constructor - The Kinetic Alphabet</title>`;
    $$payload2.out.push(`<meta name="description" content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for staffs, fans, and other flow arts. Create, learn, and share movement sequences."/>`);
  });
  $$payload.out.push(`<div class="tka-app svelte-9feqss" data-testid="tka-application">`);
  {
    $$payload.out.push("<!--[!-->");
    {
      $$payload.out.push("<!--[-->");
      LoadingScreen($$payload, {
        progress: initializationProgress,
        message: "Initializing Constructor..."
      });
    }
    $$payload.out.push(`<!--]-->`);
  }
  $$payload.out.push(`<!--]--></div>`);
  pop();
}
export {
  MainApplication as M
};
