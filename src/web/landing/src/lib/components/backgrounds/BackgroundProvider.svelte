<script lang="ts">
	// Global types are now in src/lib/types/global.d.ts
	import { browser } from '$app/environment';
	import { onDestroy, onMount } from 'svelte';
	import { setRunesBackgroundContext } from './contexts/BackgroundContext.svelte';
	import type { BackgroundType, QualityLevel } from './types/types';

	const {
		backgroundType: propBackgroundType,
		initialQuality: propInitialQuality,
		isLoading: propIsLoading,
		children,
	} = $props<{
		backgroundType?: BackgroundType;
		initialQuality?: QualityLevel | undefined;
		isLoading?: boolean;
		children?: import('svelte').Snippet;
	}>();

	let backgroundType = $state(propBackgroundType || 'snowfall');
	let initialQuality = $state(propInitialQuality);
	let isLoading = $state(propIsLoading || false);
	let isMounted = $state(false);

	$effect(() => {
		if (propBackgroundType !== undefined) {
			backgroundType = propBackgroundType;
		}
		if (propInitialQuality !== undefined) {
			initialQuality = propInitialQuality;
		}
		if (propIsLoading !== undefined) {
			isLoading = propIsLoading;
		}
	});

	let runesContext = $state<ReturnType<typeof setRunesBackgroundContext> | null>(null);
	let contextsInitialized = $state(false);

	onMount(() => {
		if (browser && !contextsInitialized) {
			const runesCtx = setRunesBackgroundContext();
			runesContext = runesCtx;
			contextsInitialized = true;

			if (typeof window !== 'undefined') {
				// Attach for debugging / external access
				(
					window as typeof window & { __runesBackgroundContext?: unknown }
				).__runesBackgroundContext = runesCtx;
			}
		}
	});

	let isUpdatingFromContext = $state(false);

	function getBackgroundTypeKey(type: BackgroundType | null): string {
		return type || 'none';
	}

	let currentBackgroundTypeKey = $state<string>('');
	let currentIsLoadingKey = $state<string>('');

	$effect(() => {
		if (!browser) return;
		if (!runesContext) return;
		if (isUpdatingFromContext) return;

		const newKey = getBackgroundTypeKey(backgroundType);

		if (newKey === currentBackgroundTypeKey) return;

		currentBackgroundTypeKey = newKey;

		if (backgroundType) {
			isUpdatingFromContext = true;
			try {
				runesContext.setBackgroundType(backgroundType);
			} finally {
				isUpdatingFromContext = false;
			}
		}
	});

	$effect(() => {
		if (!browser) return;
		if (!runesContext) return;
		if (isUpdatingFromContext) return;

		const newKey = String(isLoading);

		if (newKey === currentIsLoadingKey) return;

		currentIsLoadingKey = newKey;

		isUpdatingFromContext = true;
		try {
			runesContext.setLoading(isLoading);
		} finally {
			isUpdatingFromContext = false;
		}
	});

	function handleBackgroundChange(event: CustomEvent) {
		if (!browser || !runesContext) return;

		if (event.detail && typeof event.detail === 'string') {
			const newBackgroundType = event.detail as BackgroundType;

			if (backgroundType !== newBackgroundType) {
				backgroundType = newBackgroundType;
				runesContext.setBackgroundType(newBackgroundType);
			}
		}
	}

	onMount(() => {
		isMounted = true;

		if (!browser) {
			return;
		}

		if (!runesContext) {
			console.error('No background context available!');
			return;
		}

		if (initialQuality) {
			runesContext.setQuality(initialQuality);
		}

		window.addEventListener('changeBackground', handleBackgroundChange as EventListener);
	});

	onDestroy(() => {
		if (!browser || !runesContext) return;

		window.removeEventListener('changeBackground', handleBackgroundChange as EventListener);
		runesContext.cleanup();
	});

	const derivedType = $derived(backgroundType);
	const derivedIsLoading = $derived(isLoading);

	export const background = {
		get type() {
			return derivedType;
		},
		get isLoading() {
			return derivedIsLoading;
		},
		setType: (type: BackgroundType) => {
			if (!browser || !runesContext) return;
			backgroundType = type;
			runesContext.setBackgroundType(type);
		},
		setLoading: (loading: boolean) => {
			if (!browser || !runesContext) return;
			isLoading = loading;
			runesContext.setLoading(loading);
		},
		setQuality: (quality: QualityLevel) => {
			if (!browser || !runesContext) return;
			runesContext.setQuality(quality);
		},
	};
</script>

{#if browser && isMounted}
	{@render children?.()}
{/if}
