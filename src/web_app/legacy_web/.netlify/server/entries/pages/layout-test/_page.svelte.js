import "clsx";
import { d as ensure_array_like, q as attr, e as escape_html, a as attr_class, s as stringify, p as pop, c as push } from "../../../chunks/vendor.js";
function LayoutTest($$payload, $$props) {
  push();
  let testResults = [];
  let isRunning = false;
  const each_array = ensure_array_like(testResults);
  $$payload.out += `<div class="layout-test svelte-4d788t"><h1>Layout Test</h1> <button${attr("disabled", isRunning, true)} class="svelte-4d788t">${escape_html("Run Tests Again")}</button> <div class="test-results svelte-4d788t"><h2>Test Results</h2> <div class="results-grid svelte-4d788t"><!--[-->`;
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let result = each_array[$$index];
    $$payload.out += `<div${attr_class(`result-card ${stringify(result.success ? "success" : "error")}`, "svelte-4d788t")}><h3>${escape_html(result.title)}</h3> <p>Dimensions: ${escape_html(result.dimensions.width)}x${escape_html(result.dimensions.height)}</p> `;
    if (result.success) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<div class="image-container svelte-4d788t"><img${attr("src", result.imageUrl)} alt="Test Result" class="svelte-4d788t"/></div>`;
    } else {
      $$payload.out += "<!--[!-->";
      $$payload.out += `<div class="error-message svelte-4d788t">Error generating image</div>`;
    }
    $$payload.out += `<!--]--></div>`;
  }
  $$payload.out += `<!--]--></div></div></div>`;
  pop();
}
function _page($$payload) {
  LayoutTest($$payload);
}
export {
  _page as default
};
