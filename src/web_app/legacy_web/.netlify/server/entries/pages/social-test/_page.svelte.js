import { a as attr_class, e as escape_html, q as attr, p as pop, c as push, A as clsx } from "../../../chunks/vendor.js";
/* empty css                                                         */
function _page($$payload, $$props) {
  push();
  let isLoading = false;
  $$payload.out += `<div class="container svelte-1rx46ll"><h1 class="svelte-1rx46ll">Social Media Integration Test</h1> <div class="status-section svelte-1rx46ll"><h2>Authentication Status</h2> <ul class="svelte-1rx46ll"><li class="svelte-1rx46ll">Facebook: <span${attr_class(clsx("not-authenticated"), "svelte-1rx46ll")}>${escape_html("Not Authenticated")}</span></li> <li class="svelte-1rx46ll">Instagram: <span${attr_class(clsx("not-authenticated"), "svelte-1rx46ll")}>${escape_html("Not Authenticated")}</span></li> <li class="svelte-1rx46ll">TikTok: <span${attr_class(clsx("not-authenticated"), "svelte-1rx46ll")}>${escape_html("Not Authenticated")}</span></li></ul></div> <div class="test-section svelte-1rx46ll"><h2>Test Social Media Posting</h2> <div class="button-group svelte-1rx46ll"><button${attr("disabled", isLoading, true)} class="svelte-1rx46ll">${escape_html("Test Facebook Post")}</button> <button${attr("disabled", isLoading, true)} class="svelte-1rx46ll">${escape_html("Test Instagram Post")}</button> <button${attr("disabled", isLoading, true)} class="svelte-1rx46ll">${escape_html("Test TikTok Post")}</button> <button${attr("disabled", isLoading, true)} class="svelte-1rx46ll">${escape_html("Test Facebook Group Post")}</button></div></div> <div class="note-section svelte-1rx46ll"><h3>Notes</h3> <p>This page tests the social media integration functionality. When you click on a test button:</p> <ul class="svelte-1rx46ll"><li class="svelte-1rx46ll">If you're not authenticated, you'll be redirected to the platform's login page</li> <li class="svelte-1rx46ll">If you are authenticated, a simulated post will be attempted</li> <li class="svelte-1rx46ll">In a real implementation, the post would be sent to the platform's API</li></ul></div></div>`;
  pop();
}
export {
  _page as default
};
