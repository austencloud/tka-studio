import "clsx";
import { p as pop, a as push } from "../../../chunks/index.js";
import { M as MainApplication } from "../../../chunks/MainApplication.js";
function _page($$payload, $$props) {
  push();
  MainApplication($$payload);
  pop();
}
export {
  _page as default
};
