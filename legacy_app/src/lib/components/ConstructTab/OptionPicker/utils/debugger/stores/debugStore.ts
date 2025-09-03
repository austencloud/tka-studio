// src/lib/components/OptionPicker/utils/debugger/stores/debugStore.ts
import { writable, get } from 'svelte/store';
import { FoldableDeviceUtils } from '$lib/utils/deviceDetection';
import { activeLayoutRule } from '../../layoutUtils';

// Types
export type CopyStatus = 'idle' | 'copying' | 'copied' | 'error';

// Main visibility state
export const isDebuggerVisible = writable(false);

// Copy button states
export const copyStatus = writable<CopyStatus>('idle');
export const copyError = writable<string | null>(null);
export const currentStateCopyStatus = writable<CopyStatus>('idle');
export const currentStateCopyError = writable<string | null>(null);

// Foldable device simulation controls
export const simulateFoldable = writable(
	typeof window !== 'undefined' && localStorage.getItem('foldableDeviceOverride') ? true : false
);
export const simulatedFoldableType = writable<'zfold' | 'other'>('zfold');
export const simulatedFoldState = writable<boolean>(true);

// Initialize values from existing override if available
try {
	const existingOverride = typeof window !== 'undefined' ? localStorage.getItem('foldableDeviceOverride') : null;
	if (existingOverride) {
		const settings = JSON.parse(existingOverride);
		simulatedFoldableType.set(settings.foldableType || 'zfold');
		simulatedFoldState.set(settings.isUnfolded);
	}
} catch (e) {
	console.error('Error reading existing foldable override:', e);
}

// Timeout IDs
let copyTimeoutId: ReturnType<typeof setTimeout> | null = null;
let currentStateCopyTimeoutId: ReturnType<typeof setTimeout> | null = null;

// Actions
export const debugActions = {
	toggleDebugger() {
		isDebuggerVisible.update((value) => !value);
		if (!get(isDebuggerVisible)) this.resetCopyStates();
	},

	resetCopyStates() {
		clearTimeout(copyTimeoutId || undefined);
		copyStatus.set('idle');
		copyError.set(null);
		copyTimeoutId = null;

		clearTimeout(currentStateCopyTimeoutId || undefined);
		currentStateCopyStatus.set('idle');
		currentStateCopyError.set(null);
		currentStateCopyTimeoutId = null;
	},

	applyFoldableSimulation() {
		const isSimulating = get(simulateFoldable);
		if (isSimulating) {
			FoldableDeviceUtils.setManualOverride({
				isFoldable: true,
				foldableType: get(simulatedFoldableType),
				isUnfolded: get(simulatedFoldState)
			});
		} else {
			FoldableDeviceUtils.clearManualOverride();
		}

		const message = isSimulating
			? 'Foldable device simulation settings applied! Page reload required to apply changes. Reload now?'
			: 'Foldable device simulation disabled! Page reload required to apply changes. Reload now?';

		if (confirm(message)) window.location.reload();
	},

	async copyToClipboard(
		textBuilder: () => string,
		statusStore: typeof copyStatus,
		errorStore: typeof copyError,
		timeoutSetter: (tid: ReturnType<typeof setTimeout> | null) => void
	) {
		clearTimeout(
			statusStore === copyStatus
				? (copyTimeoutId as unknown as number | undefined)
				: (currentStateCopyTimeoutId as unknown as number | undefined)
		);
		if (!navigator.clipboard) {
			errorStore.set('Clipboard API not available.');
			statusStore.set('error');
			resetStatusAfterDelay(statusStore, errorStore, timeoutSetter);
			return;
		}

		statusStore.set('copying');
		errorStore.set(null);

		try {
			await navigator.clipboard.writeText(textBuilder());
			statusStore.set('copied');
		} catch (err) {
			errorStore.set('Failed to copy.');
			statusStore.set('error');
			console.error('Failed to copy text:', err);
		} finally {
			resetStatusAfterDelay(statusStore, errorStore, timeoutSetter);
		}
	},
	// Get debug info text without copying (for CopyButton)
	async getDebugInfoText(layoutContext?: any): Promise<string> {
		return buildDebugInfoText(layoutContext);
	},

	async copyDebugInfo(layoutContext?: any) {
		await this.copyToClipboard(
			() => buildDebugInfoText(layoutContext),
			copyStatus,
			copyError,
			(tid) => {
				copyTimeoutId = tid;
			}
		);
	},

	async copyCurrentState(layoutContext: any) {
		await this.copyToClipboard(
			() => buildCurrentStateText(layoutContext),
			currentStateCopyStatus,
			currentStateCopyError,
			(tid) => {
				currentStateCopyTimeoutId = tid;
			}
		);
	},

	cleanup() {
		clearTimeout(copyTimeoutId || undefined);
		clearTimeout(currentStateCopyTimeoutId || undefined);
	}
};

// Helpers
function buildDebugInfoText(layoutContext?: any): string {
	const rule = get(activeLayoutRule);
	let text = rule
		? `Active Layout Rule:\nDescription: ${rule.description}\nColumns: ${rule.columns}${
				rule.maxColumns ? ` (Max: ${rule.maxColumns})` : ''
			}\n${buildConditionsText(rule.when)}`
		: 'Active Layout Rule: None Matched\n';

	text += `\n${buildCurrentStateText(layoutContext)}`;
	text += `\n\nFoldable Device Detection:\n${JSON.stringify(FoldableDeviceUtils.getDebugInfo(), null, 2)}`;
	return text;
}

function buildConditionsText(conditions: any): string {
	if (!conditions) return '';
	return `Conditions:\n${Object.entries(conditions)
		.map(([key, value]) => `  - ${key}: ${value}`)
		.join('\n')}`;
}

export function buildCurrentStateText(layoutContext: any): string {
	if (!layoutContext) return 'Layout context not available';

	const foldableInfo = layoutContext.foldableInfo || {
		isFoldable: false,
		isUnfolded: false,
		foldableType: 'unknown',
		confidence: 0
	};

	const activeRule = get(activeLayoutRule);
	const ua = typeof navigator !== 'undefined' ? navigator.userAgent : 'Unknown';
	const uaShort = ua.substring(0, 80) + (ua.length > 80 ? '...' : '');
	return `Current State:
  - Active Rule: ${activeRule?.description || 'No rule matched'}
  - Columns: ${layoutContext.layoutConfig.gridColumns.match(/repeat\((\d+)\)/)?.[1] || 'unknown'}
  - Device: ${layoutContext.deviceType} (${layoutContext.isMobile ? 'mobile' : 'desktop'})
  - Foldable: ${foldableInfo.isFoldable ? 'Yes' : 'No'}
${
	foldableInfo.isFoldable
		? `  - Type: ${foldableInfo.foldableType}
  - Unfolded: ${foldableInfo.isUnfolded ? 'Yes' : 'No'}
  - Detection: ${foldableInfo.detectionMethod || 'Unknown'}
  - Confidence: ${foldableInfo.confidence || 'N/A'}`
		: ''
}
  - Aspect: ${layoutContext.containerAspect}
  - Orientation: ${layoutContext.isPortrait ? 'portrait' : 'landscape'}
  - Size: ${layoutContext.containerWidth}×${layoutContext.containerHeight}
  - Pixel Ratio: ${typeof window !== 'undefined' ? window.devicePixelRatio : 'N/A'}
  - User Agent: ${uaShort}`;
}

function resetStatusAfterDelay(
	statusStore: typeof copyStatus,
	errorStore: typeof copyError,
	timeoutSetter: (tid: ReturnType<typeof setTimeout> | null) => void,
	delay = 2000
) {
	const tid = setTimeout(() => {
		statusStore.set('idle');
		errorStore.set(null);
		timeoutSetter(null);
	}, delay);
	timeoutSetter(tid);
}
