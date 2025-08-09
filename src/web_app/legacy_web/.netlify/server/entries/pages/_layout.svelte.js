import { f as fallback, a as attr_class, h as html, e as escape_html, b as bind_props, p as pop, c as push, s as stringify, d as ensure_array_like, g as store_get, u as unsubscribe_stores, w as writable, o as onDestroy, i as slot } from "../../chunks/vendor.js";
import "../../chunks/uiStore.js";
import "clsx";
/* empty css                                                      */
class InjectableErrorHandlingService {
  enabled = true;
  constructor() {
    if (typeof window !== "undefined") {
      this.setupGlobalErrorHandlers();
    }
  }
  setupGlobalErrorHandlers() {
    window.addEventListener("error", (event) => {
      this.handleError(new Error(event.message), "high", {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      });
    });
    window.addEventListener("unhandledrejection", (event) => {
      this.handleError(new Error(`Unhandled Promise Rejection: ${event.reason}`), "high");
    });
  }
  handleError(error, severity = "medium", context) {
    if (!this.enabled) return;
    console.error(`[${severity.toUpperCase()}] ${error.message}`, { error, context });
  }
  reportError(error, context) {
    this.handleError(error, "high", context);
  }
  enable() {
    this.enabled = true;
  }
  disable() {
    this.enabled = false;
  }
  isEnabled() {
    return this.enabled;
  }
}
new InjectableErrorHandlingService();
class BackgroundServiceImpl {
  currentBackground = "snowfall";
  enabled = true;
  constructor() {
    if (typeof localStorage !== "undefined") {
      this.loadPreferences();
    }
  }
  getCurrentBackground() {
    return this.currentBackground;
  }
  setBackground(type) {
    this.currentBackground = type;
    this.savePreferences();
    this.emitBackgroundChange(type);
  }
  isEnabled() {
    return this.enabled;
  }
  enable() {
    this.enabled = true;
    this.savePreferences();
  }
  disable() {
    this.enabled = false;
    this.savePreferences();
  }
  loadPreferences() {
    if (typeof localStorage === "undefined") return;
    try {
      const saved = localStorage.getItem("tka-background-preferences");
      if (saved) {
        const preferences = JSON.parse(saved);
        this.currentBackground = preferences.background || "snowfall";
        this.enabled = preferences.enabled !== false;
      }
    } catch (error) {
      console.warn("Failed to load background preferences:", error);
    }
  }
  savePreferences() {
    if (typeof localStorage === "undefined") return;
    try {
      const preferences = {
        background: this.currentBackground,
        enabled: this.enabled
      };
      localStorage.setItem("tka-background-preferences", JSON.stringify(preferences));
    } catch (error) {
      console.warn("Failed to save background preferences:", error);
    }
  }
  emitBackgroundChange(type) {
    if (typeof document === "undefined") return;
    const event = new CustomEvent("background-changed", {
      detail: { type },
      bubbles: true
    });
    document.dispatchEvent(event);
  }
}
new BackgroundServiceImpl();
function Toast($$payload, $$props) {
  push();
  let icon;
  let message = $$props["message"];
  let type = fallback($$props["type"], "info");
  let duration = fallback($$props["duration"], 5e3);
  let showCloseButton = fallback($$props["showCloseButton"], true);
  let action = fallback($$props["action"], null);
  icon = {
    success: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
    error: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>',
    warning: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
    info: '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
  }[type];
  {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div${attr_class(`toast-container ${stringify(type)}`, "svelte-1yudb1")}><div class="toast-icon svelte-1yudb1" aria-hidden="true">${html(icon)}</div> <div class="toast-content svelte-1yudb1"><div class="toast-message svelte-1yudb1">${escape_html(message)}</div> `;
    if (action) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<button class="toast-action svelte-1yudb1">${escape_html(action.label)}</button>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div> `;
    if (showCloseButton) {
      $$payload.out += "<!--[-->";
      $$payload.out += `<button class="toast-close svelte-1yudb1" aria-label="Close notification"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>`;
    } else {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div>`;
  }
  $$payload.out += `<!--]-->`;
  bind_props($$props, { message, type, duration, showCloseButton, action });
  pop();
}
const toasts = writable([]);
function ToastManager($$payload, $$props) {
  push();
  var $$store_subs;
  const each_array = ensure_array_like(store_get($$store_subs ??= {}, "$toasts", toasts));
  $$payload.out += `<div class="toast-manager svelte-1w631wj"><!--[-->`;
  for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
    let toast = each_array[$$index];
    $$payload.out += `<div class="toast-wrapper svelte-1w631wj">`;
    Toast($$payload, {
      message: toast.message,
      type: toast.type,
      duration: 0,
      action: toast.action
    });
    $$payload.out += `<!----></div>`;
  }
  $$payload.out += `<!--]--></div>`;
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
function SettingsManager($$payload, $$props) {
  push();
  onDestroy(() => {
    return;
  });
  $$payload.out += `<div style="display: none;" aria-hidden="true">`;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div>`;
  pop();
}
function ServiceProvider($$payload, $$props) {
  push();
  {
    $$payload.out += "<!--[-->";
    SettingsManager($$payload);
    $$payload.out += `<!----> <!---->`;
    slot($$payload, $$props, "default", {});
    $$payload.out += `<!---->`;
  }
  $$payload.out += `<!--]-->`;
  pop();
}
function _layout($$payload, $$props) {
  push();
  let data = $$props["data"];
  if (data.error) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="layout-load-error svelte-1vd1i36"><h1 class="svelte-1vd1i36">Application Initialization Error</h1> <p>Could not load essential data: ${escape_html(data.error)}</p> <p>Please try refreshing the page.</p> `;
    {
      $$payload.out += "<!--[!-->";
    }
    $$payload.out += `<!--]--></div>`;
  } else {
    $$payload.out += "<!--[!-->";
    ServiceProvider($$payload, {
      children: ($$payload2) => {
        $$payload2.out += `<!---->`;
        slot($$payload2, $$props, "default", {});
        $$payload2.out += `<!---->`;
      },
      $$slots: { default: true }
    });
  }
  $$payload.out += `<!--]--> `;
  ToastManager($$payload);
  $$payload.out += `<!----> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]-->`;
  bind_props($$props, { data });
  pop();
}
export {
  _layout as default
};
