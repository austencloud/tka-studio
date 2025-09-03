<!-- src/lib/components/OptionPicker/utils/debugger/LayoutDebugger.svelte -->
<script lang="ts">
	import { onDestroy, getContext } from 'svelte';
	import { fade } from 'svelte/transition';
	import { LAYOUT_CONTEXT_KEY, type LayoutContext } from '../../layoutContext';
	import { activeLayoutRule } from '../layoutUtils';

	// Import components
	import DebugToggleButton from './components/DebugToggleButton.svelte';
	import ActiveRulePanel from './components/ActiveRulePanel.svelte';
	import CurrentStatePanel from './components/CurrentStatePanel.svelte';
	import FoldableControls from './components/FoldableControls.svelte';
	import DebugActions from './components/DebugActions.svelte';

	// Get layout context
	const layoutContext = getContext<LayoutContext>(LAYOUT_CONTEXT_KEY);

	// State
	let showInfo = false;

	// --- Event Handlers ---
	function toggleInfo() {
	  showInfo = !showInfo;
	}

	// Clean up on component destruction
	onDestroy(() => {
	  // Cleanup will be handled in child components
	});
  </script>

  <div class="debug-button-container">
	<DebugToggleButton {toggleInfo} />

	{#if showInfo}
	  <div class="debug-info" transition:fade={{ duration: 200 }}>
		<button
		  class="close-button"
		  on:click={toggleInfo}
		  title="Close debug info"
		  aria-label="Close debug info"
		>
		  &times;
		</button>
		<div class="rule-card">
		  <ActiveRulePanel activeRule={$activeLayoutRule} />

		  <CurrentStatePanel layoutContext={$layoutContext} />

		  <FoldableControls />

		  <DebugActions layoutContext={$layoutContext} />
		</div>
	  </div>
	{/if}
  </div>

  <style>
	/* --- Base Container and Toggle Button --- */
	.debug-button-container {
	  position: absolute;
	  bottom: 10px;
	  right: 10px;
	  z-index: 1000;
	}

	/* --- Debug Info Panel --- */
	.debug-info {
	  position: absolute;
	  bottom: 50px;
	  right: 0;
	  background: #0f172a;
	  color: #e2e8f0;
	  border: 1px solid #334155;
	  border-radius: 8px;
	  width: 320px;
	  max-height: 450px;
	  overflow-y: auto;
	  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	  padding: 0; /* Remove padding here */
	  font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas,
		'DejaVu Sans Mono', monospace;
	  font-size: 12px;
	  line-height: 1.5;
	}

	.close-button {
	  /* Panel close button */
	  position: absolute;
	  top: 8px;
	  right: 8px;
	  background: transparent;
	  border: none;
	  color: #94a3b8; /* slate-400 */
	  font-size: 20px; /* Larger X */
	  line-height: 1;
	  padding: 2px 5px;
	  cursor: pointer;
	  z-index: 10;
	  transition: color 0.2s ease;
	  border-radius: 4px;
	}

	.close-button:hover {
	  color: #f87171;
	  background-color: rgba(255, 255, 255, 0.1);
	} /* rose-400 */

	.rule-card {
	  padding: 16px;
	  padding-top: 36px; /* Space for close button */
	}

	/* --- Scrollbar --- */
	.debug-info::-webkit-scrollbar {
	  width: 6px;
	}

	.debug-info::-webkit-scrollbar-track {
	  background: #1e293b;
	  border-radius: 3px;
	}

	.debug-info::-webkit-scrollbar-thumb {
	  background-color: #475569;
	  border-radius: 3px;
	}

	.debug-info::-webkit-scrollbar-thumb:hover {
	  background-color: #64748b;
	}

	/* --- Edit Tip --- */
	:global(.edit-tip) {
	  font-size: 10px;
	  color: #94a3b8;
	  border-top: 1px solid #334155;
	  padding-top: 8px;
	  margin-top: 12px;
	}

	:global(.edit-tip code) {
	  background: #334155;
	  padding: 2px 5px;
	  border-radius: 3px;
	  color: #7dd3fc;
	}

	/* --- Actions Area --- */
	:global(.actions-area) {
	  margin-top: 12px;
	  padding-top: 8px;
	  border-top: 1px solid #334155;
	  display: flex;
	  justify-content: flex-end;
	  align-items: center;
	  gap: 8px;
	}

	/* --- Copy Button Base Styles --- */
	:global(.copy-button-base) {
	  display: inline-flex;
	  align-items: center;
	  gap: 5px;
	  border: 1px solid #475569;
	  padding: 6px 10px;
	  border-radius: 4px;
	  cursor: pointer;
	  font-weight: 500;
	  transition: all 0.2s ease-out;
	  overflow: hidden;
	  position: relative;
	}

	:global(.copy-button) {
	  background-color: #334155;
	  color: #cbd5e1;
	  font-size: 11px;
	}

	/* Animation keyframes */
	@keyframes pulse-success {
	  0% { transform: scale(1); }
	  50% { transform: scale(1.05); }
	  100% { transform: scale(1); }
	}

	@keyframes shake-error {
	  0%, 100% { transform: translateX(0); }
	  25% { transform: translateX(-3px); }
	  50% { transform: translateX(3px); }
	  75% { transform: translateX(-3px); }
	}

	@keyframes spin {
	  0% { transform: rotate(0deg); }
	  100% { transform: rotate(360deg); }
	}
  </style>
