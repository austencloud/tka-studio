import { e as escape_html, p as pop, c as push } from "../../../../../chunks/vendor.js";
import "clsx";
function _page($$payload, $$props) {
  push();
  $$payload.out += `<div class="auth-callback-container svelte-ics9ac"><div class="auth-callback-card svelte-ics9ac"><h1 class="svelte-ics9ac">Authentication ${escape_html("in progress")}</h1> `;
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="loading-spinner svelte-ics9ac"><i class="fa-solid fa-spinner fa-spin"></i></div> <p class="svelte-ics9ac">Processing your authentication...</p>`;
  }
  $$payload.out += `<!--]--></div></div>`;
  pop();
}
export {
  _page as default
};
