import { a as attr_class, e as escape_html, q as attr, d as ensure_array_like, p as pop, c as push } from "../../../chunks/vendor.js";
import { u as useContainer } from "../../../chunks/svelte5-integration.svelte.js";
import { s as sequenceContainer } from "../../../chunks/SequenceContainer.js";
function ModernStateExample($$payload, $$props) {
  push();
  let beatName = "";
  let isDarkTheme = false;
  let theme = "light";
  let isGenerating = false;
  const sequence = useContainer(sequenceContainer);
  $$payload.out += `<div${attr_class("container svelte-1ggfdxl", void 0, { "dark": isDarkTheme })}><header class="svelte-1ggfdxl"><h1 class="svelte-1ggfdxl">State Management Example (Svelte 5 + XState 5)</h1> <button class="svelte-1ggfdxl">Toggle Theme (${escape_html(theme)})</button></header> <div class="sequence-controls"><h2 class="svelte-1ggfdxl">Sequence Controls</h2> <div class="control-group svelte-1ggfdxl"><button${attr("disabled", isGenerating, true)} class="svelte-1ggfdxl">Generate Sequence</button> <button${attr("disabled", sequence.beats.length === 0, true)} class="svelte-1ggfdxl">Clear Sequence</button></div> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--> `;
  {
    $$payload.out += "<!--[!-->";
  }
  $$payload.out += `<!--]--></div> <div class="add-beat-form svelte-1ggfdxl"><h2 class="svelte-1ggfdxl">Add Beat</h2> <form class="svelte-1ggfdxl"><input type="text"${attr("value", beatName)} placeholder="Beat name"${attr("disabled", isGenerating, true)} class="svelte-1ggfdxl"/> <button type="submit"${attr("disabled", !beatName.trim() || isGenerating, true)} class="svelte-1ggfdxl">Add Beat</button></form></div> <div class="sequence-display svelte-1ggfdxl"><h2 class="svelte-1ggfdxl">Sequence (${escape_html(sequence.beats.length)} beats)</h2> `;
  if (sequence.beats.length === 0) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="empty-state svelte-1ggfdxl">No beats in sequence. Generate or add beats to get started.</div>`;
  } else {
    $$payload.out += "<!--[!-->";
    const each_array = ensure_array_like(sequence.beats);
    $$payload.out += `<ul class="beat-list svelte-1ggfdxl"><!--[-->`;
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let beat = each_array[$$index];
      $$payload.out += `<div${attr_class("beat-item svelte-1ggfdxl", void 0, { "selected": sequence.selectedBeatIds.includes(beat.id) })} tabindex="0" role="button"><div class="beat-content svelte-1ggfdxl"><span class="beat-index svelte-1ggfdxl">${escape_html(beat.number)}</span> <span class="beat-name svelte-1ggfdxl">${escape_html(beat.letter || `Beat ${beat.number}`)}</span> <span class="beat-value svelte-1ggfdxl">${escape_html(beat.id.substring(0, 8))}</span></div> <button class="remove-button svelte-1ggfdxl"${attr("aria-label", `Remove beat ${beat.number}`)}>✕</button></div>`;
    }
    $$payload.out += `<!--]--></ul>`;
  }
  $$payload.out += `<!--]--></div> <div class="selection-info svelte-1ggfdxl"><h2 class="svelte-1ggfdxl">Selected Beats (${escape_html(sequence.selectedBeatIds.length)})</h2> `;
  if (sequence.selectedBeatIds.length === 0) {
    $$payload.out += "<!--[-->";
    $$payload.out += `<div class="empty-state svelte-1ggfdxl">No beats selected. Click on a beat to select it.</div>`;
  } else {
    $$payload.out += "<!--[!-->";
    const each_array_1 = ensure_array_like(sequence.beats.filter((beat) => sequence.selectedBeatIds.includes(beat.id)));
    $$payload.out += `<ul class="selected-beats svelte-1ggfdxl"><!--[-->`;
    for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
      let beat = each_array_1[$$index_1];
      $$payload.out += `<li class="svelte-1ggfdxl">Beat ${escape_html(beat.number)} - ${escape_html(beat.letter || "Unnamed")}</li>`;
    }
    $$payload.out += `<!--]--></ul>`;
  }
  $$payload.out += `<!--]--></div></div>`;
  pop();
}
function _page($$payload) {
  let showModernExample = false;
  $$payload.out += `<div class="container svelte-hfxxhp"><h1 class="svelte-hfxxhp">State Management Examples</h1> <div class="tabs svelte-hfxxhp"><button${attr_class("svelte-hfxxhp", void 0, { "active": !showModernExample })}>Current Approach</button> <button${attr_class("svelte-hfxxhp", void 0, { "active": showModernExample })}>Modern Approach</button></div> `;
  {
    $$payload.out += "<!--[!-->";
    $$payload.out += `<div class="example-container svelte-hfxxhp"><p class="description svelte-hfxxhp">This example demonstrates the current state management system using XState and Svelte
				stores. Open your browser's developer console to see state changes.</p> `;
    ModernStateExample($$payload);
    $$payload.out += `<!----> <div class="info svelte-hfxxhp"><h2 class="svelte-hfxxhp">Current State Management</h2> <p>The current state management system uses:</p> <ul class="svelte-hfxxhp"><li class="svelte-hfxxhp"><strong>XState</strong> for complex state machines</li> <li class="svelte-hfxxhp"><strong>Svelte stores</strong> for reactive state</li> <li class="svelte-hfxxhp"><strong>State registry</strong> for centralized state management</li></ul> <p>Try interacting with the example above to see how state changes are handled.</p></div></div>`;
  }
  $$payload.out += `<!--]--></div>`;
}
export {
  _page as default
};
