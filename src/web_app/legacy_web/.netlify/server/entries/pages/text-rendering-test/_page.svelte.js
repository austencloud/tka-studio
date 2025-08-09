import "clsx";
import { q as attr, e as escape_html, d as ensure_array_like, a as attr_class, p as pop, c as push } from "../../../chunks/vendor.js";
function TextRenderingTest($$payload, $$props) {
  push();
  let testSizes = [
    // Standard export sizes
    { width: 950, height: 950, label: "1x1 Grid" },
    { width: 1900, height: 950, label: "2x1 Grid" },
    { width: 2850, height: 950, label: "3x1 Grid" },
    { width: 1900, height: 1900, label: "2x2 Grid" },
    { width: 2850, height: 1900, label: "3x2 Grid" },
    { width: 3800, height: 1900, label: "4x2 Grid" },
    { width: 2850, height: 2850, label: "3x3 Grid" },
    { width: 3800, height: 2850, label: "4x3 Grid" },
    { width: 3800, height: 3800, label: "4x4 Grid" }
  ];
  let testSequences = [
    // 1-row layouts
    { beats: 1, title: "One Beat (1 row)", difficulty: 1 },
    { beats: 2, title: "Two Beats (1 row)", difficulty: 1 },
    { beats: 3, title: "Three Beats (1 row)", difficulty: 1 },
    { beats: 4, title: "Four Beats (1 row)", difficulty: 1 },
    // 2-row layouts
    { beats: 5, title: "Five Beats (2 rows)", difficulty: 2 },
    { beats: 6, title: "Six Beats (2 rows)", difficulty: 2 },
    { beats: 8, title: "Eight Beats (2 rows)", difficulty: 2 },
    // 3-row layouts
    { beats: 9, title: "Nine Beats (3 rows)", difficulty: 3 },
    { beats: 12, title: "Twelve Beats (3 rows)", difficulty: 3 },
    // 4-row layouts
    { beats: 16, title: "Sixteen Beats (4 rows)", difficulty: 4 },
    { beats: 20, title: "Twenty Beats (4 rows)", difficulty: 5 }
  ];
  let testResults = [];
  let isRunningTests = false;
  $$payload.out += `<div class="text-rendering-test svelte-1ok1ded"><h1>Text Rendering Test</h1> <button${attr("disabled", isRunningTests, true)} class="svelte-1ok1ded">${escape_html("Run Tests")}</button> <div class="test-results svelte-1ok1ded"><h2>Test Results (${escape_html(testResults.length)} of ${escape_html(testSizes.length * testSequences.length)})</h2> `;
  if (testResults.length === 0 && isRunningTests) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<p>Running tests, please wait...</p>`;
  } else if (testResults.length === 0) {
    $$payload.out += "<!--[1-->";
    $$payload.out += `<p>No test results yet. Click "Run Tests" to start.</p>`;
  } else {
    $$payload.out += "<!--[!-->";
    const each_array = ensure_array_like(testResults);
    $$payload.out += `<div class="results-grid svelte-1ok1ded"><!--[-->`;
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let result = each_array[$$index];
      $$payload.out += `<div${attr_class("result-card svelte-1ok1ded", void 0, { "success": result.success, "error": !result.success })}><h3 class="svelte-1ok1ded">${escape_html(result.size)}</h3> <h4 class="svelte-1ok1ded">${escape_html(result.sequence)}</h4> `;
      if (result.success) {
        $$payload.out += "<!--[-->";
        $$payload.out += `<div class="image-container svelte-1ok1ded"><img${attr("src", result.imageUrl)}${attr("alt", `${result.sequence} at ${result.size}`)} class="svelte-1ok1ded"/></div>`;
      } else {
        $$payload.out += "<!--[!-->";
        $$payload.out += `<div class="error-message svelte-1ok1ded"><p>Error: ${escape_html(result.error)}</p></div>`;
      }
      $$payload.out += `<!--]--></div>`;
    }
    $$payload.out += `<!--]--></div>`;
  }
  $$payload.out += `<!--]--></div> <div class="test-container svelte-1ok1ded"></div></div>`;
  pop();
}
function _page($$payload) {
  TextRenderingTest($$payload);
}
export {
  _page as default
};
