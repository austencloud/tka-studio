<script lang="ts">
	// Button state as string literal type instead of enum
	type ButtonStateType = 'normal' | 'active' | 'disabled' | 'loading';

	// Button state constants
	const BUTTON_STATE = {
		NORMAL: 'normal' as const,
		ACTIVE: 'active' as const,
		DISABLED: 'disabled' as const,
		LOADING: 'loading' as const
	};

	// Props with defaults using $props() from Svelte 5
	const {
		label = '',
		icon = null,
		iconPosition = 'left',
		buttonState = BUTTON_STATE.NORMAL,
		disabled = false,
		loading = false,
		customClass = '',
		variant = 'blue',
		size = 'medium',
		title = null,
		fullWidth = false,
		type = 'button',
		pressed = null,
		form = null
	} = $props<{
		label?: string;
		icon?: string | null;
		iconPosition?: 'left' | 'right' | 'only';
		buttonState?: ButtonStateType;
		disabled?: boolean;
		loading?: boolean;
		customClass?: string;
		variant?: 'blue' | 'dark' | 'ghost' | 'success' | 'danger';
		size?: 'small' | 'medium' | 'large';
		title?: string | null;
		fullWidth?: boolean;
		type?: 'button' | 'submit' | 'reset';
		pressed?: boolean | null;
		form?: string | null;
	}>();

	// Event handling with Svelte 5 approach
	const dispatch = (name: string, detail?: any) => {
		const event = new CustomEvent(name, { detail });
		dispatchEvent(event);
	};

	// Internal state
	let spinnerVisible = $state(false);

	// Handle opacity for gradients
	const OPACITY = 0.9;

	// Define gradients based on variants and states
	const gradients = {
		blue: {
			normal: `
				background: linear-gradient(
					135deg,
					#1e3c72 0%,
					#6c9ce9 30%,
					#4a77d4 60%,
					#2a52be 100%
				);
			`,
			hover: `
				background: linear-gradient(
					135deg,
					#264f94 0%,
					#7baafb 30%,
					#5584e1 60%,
					#3563cf 100%
				);
			`,
			active: `
				background: linear-gradient(
					135deg,
					#16295a 0%,
					#517bbd 30%,
					#3a62ab 60%,
					#1d3b8c 100%
				);
			`
		},
		dark: {
			normal: `
				background: linear-gradient(
					135deg,
					rgba(40, 40, 40, ${OPACITY}) 0%,
					rgba(55, 55, 55, ${OPACITY}) 50%,
					rgba(70, 70, 70, ${OPACITY}) 100%
				);
			`,
			hover: `
				background: linear-gradient(
					135deg,
					rgba(80, 80, 80, ${OPACITY}) 0%,
					rgba(160, 160, 160, ${OPACITY}) 30%,
					rgba(120, 120, 120, ${OPACITY}) 60%,
					rgba(40, 40, 40, ${OPACITY}) 100%
				);
			`,
			active: `
				background: linear-gradient(
					135deg,
					#1e3c72 0%,
					#6c9ce9 30%,
					#4a77d4 60%,
					#2a52be 100%
				);
			`
		},
		ghost: {
			normal: `
				background: rgba(70, 70, 70, 0.7);
			`,
			hover: `
				background: rgba(100, 100, 100, 0.8);
			`,
			active: `
				background: linear-gradient(
					135deg,
					#1e3c72 0%,
					#6c9ce9 30%,
					#4a77d4 60%,
					#2a52be 100%
				);
			`
		},
		success: {
			normal: `
				background: linear-gradient(
					135deg,
					#0b4d26 0%,
					#2e8c50 30%,
					#1f7a3d 60%,
					#0d5e2f 100%
				);
			`,
			hover: `
				background: linear-gradient(
					135deg,
					#0d5e2f 0%,
					#34a05c 30%,
					#24904a 60%,
					#0f6f35 100%
				);
			`,
			active: `
				background: linear-gradient(
					135deg,
					#07341a 0%,
					#206d3c 30%,
					#155c2a 60%,
					#093d20 100%
				);
			`
		},
		danger: {
			normal: `
				background: linear-gradient(
					135deg,
					#8b0000 0%,
					#d32f2f 30%,
					#b71c1c 60%,
					#7f0000 100%
				);
			`,
			hover: `
				background: linear-gradient(
					135deg,
					#a50000 0%,
					#ef5350 30%,
					#d32f2f 60%,
					#9a0000 100%
				);
			`,
			active: `
				background: linear-gradient(
					135deg,
					#6d0000 0%,
					#b71c1c 30%,
					#8b0000 60%,
					#5d0000 100%
				);
			`
		}
	};

	// Define colors based on variants and states
	const colors = {
		blue: {
			normal: 'white',
			hover: 'white',
			active: 'white',
			disabled: '#aaaaaa'
		},
		dark: {
			normal: 'white',
			hover: 'white',
			active: 'white',
			disabled: '#888888'
		},
		ghost: {
			normal: 'white',
			hover: 'white',
			active: 'white',
			disabled: '#888888'
		},
		success: {
			normal: 'white',
			hover: 'white',
			active: 'white',
			disabled: '#aaaaaa'
		},
		danger: {
			normal: 'white',
			hover: 'white',
			active: 'white',
			disabled: '#aaaaaa'
		}
	};

	// Border colors
	const borders = {
		blue: {
			normal: 'rgba(255, 255, 255, 0.5)',
			hover: 'white',
			active: 'white',
			disabled: 'rgba(255, 255, 255, 0.3)'
		},
		dark: {
			normal: 'rgba(255, 255, 255, 0.3)',
			hover: 'rgba(255, 255, 255, 0.6)',
			active: 'rgba(255, 255, 255, 0.7)',
			disabled: 'rgba(255, 255, 255, 0.2)'
		},
		ghost: {
			normal: 'rgba(255, 255, 255, 0.5)',
			hover: 'rgba(255, 255, 255, 0.7)',
			active: 'rgba(255, 255, 255, 0.8)',
			disabled: 'rgba(255, 255, 255, 0.3)'
		},
		success: {
			normal: 'rgba(255, 255, 255, 0.5)',
			hover: 'white',
			active: 'white',
			disabled: 'rgba(255, 255, 255, 0.3)'
		},
		danger: {
			normal: 'rgba(255, 255, 255, 0.5)',
			hover: 'white',
			active: 'white',
			disabled: 'rgba(255, 255, 255, 0.3)'
		}
	};

	// Handle icon spacing based on label presence and position
	const iconSpacing = $derived(icon && label && iconPosition !== 'only' ? '0.5rem' : '0');

	// Compute actual state based on disabled and loading props
	const actualState = $derived(
		disabled ? BUTTON_STATE.DISABLED : loading ? BUTTON_STATE.LOADING : buttonState
	);

	// Update spinner visibility with slight delay to avoid flashing
	$effect(() => {
		if (loading) {
			setTimeout(() => {
				spinnerVisible = loading;
			}, 100);
		} else {
			spinnerVisible = false;
		}
	});

	// Function to compute appropriate styles (memoized for performance)
	const styleCache = new Map();

	function computeButtonStyles(
		variant: 'blue' | 'dark' | 'ghost' | 'success' | 'danger',
		state: ButtonStateType,
		isFullWidth: boolean
	): string {
		const cacheKey = `${variant}-${state}-${isFullWidth}`;

		if (styleCache.has(cacheKey)) {
			return styleCache.get(cacheKey);
		}

		let result = '';

		// For disabled state
		if (state === BUTTON_STATE.DISABLED) {
			if (variant === 'blue') {
				result = `
					background: linear-gradient(
						135deg,
						rgba(30, 60, 114, 0.5) 0%,
						rgba(108, 156, 233, 0.5) 30%,
						rgba(74, 119, 212, 0.5) 60%,
						rgba(42, 82, 190, 0.5) 100%
					);
					color: ${colors[variant].disabled};
					border-color: ${borders[variant].disabled};
					pointer-events: none;
				`;
			} else {
				result = `
					opacity: 0.6;
					color: ${colors[variant].disabled};
					border-color: ${borders[variant].disabled};
					${gradients[variant].normal}
					pointer-events: none;
				`;
			}
		}
		// For loading state
		else if (state === BUTTON_STATE.LOADING) {
			result = `
				${gradients[variant].normal}
				color: ${colors[variant].normal};
				border-color: ${borders[variant].normal};
				position: relative;
				pointer-events: none;
			`;
		}
		// For active state
		else if (state === BUTTON_STATE.ACTIVE) {
			result = `
				${gradients[variant].normal}
				color: ${colors[variant].active};
				border-color: ${borders[variant].active};
				box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
			`;
		}
		// Normal state
		else {
			result = `
				${gradients[variant].normal}
				color: ${colors[variant].normal};
				border-color: ${borders[variant].normal};
			`;
		}

		// Add full width if needed
		if (isFullWidth) {
			result += `width: 100%;`;
		}

		styleCache.set(cacheKey, result);
		return result;
	}

	// Get current style based on variant, state, disabled and fullWidth
	const buttonStyles = $derived(computeButtonStyles(variant, actualState, fullWidth));

	// Click handler
	function handleClick(event: MouseEvent) {
		if (!disabled && !loading) {
			dispatch('click', event);
		}
	}

	function handleFocus(event: FocusEvent) {
		dispatch('focus', event);
	}

	function handleBlur(event: FocusEvent) {
		dispatch('blur', event);
	}
</script>

<button
	class="metallic-button {size} {variant} {actualState} {customClass}"
	class:full-width={fullWidth}
	{disabled}
	{title}
	{type}
	{form}
	style={buttonStyles}
	aria-disabled={disabled || loading}
	aria-busy={loading}
	aria-pressed={pressed}
	onclick={handleClick}
	onfocus={handleFocus}
	onblur={handleBlur}
>
	{#if loading && spinnerVisible}
		<div class="spinner">
			<svg class="spinner-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
				<circle
					class="spinner-circle"
					cx="12"
					cy="12"
					r="10"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
				/>
			</svg>
		</div>
	{:else}
		{#if icon && (iconPosition === 'left' || iconPosition === 'only')}
			<div
				class="icon"
				style={`margin-right: ${label && iconPosition !== 'only' ? iconSpacing : 0}`}
			>
				<img src={icon} alt="" aria-hidden="true" />
			</div>
		{/if}

		{#if label && iconPosition !== 'only'}
			<span>{label}</span>
		{/if}

		{#if icon && iconPosition === 'right'}
			<div class="icon" style={`margin-left: ${label ? iconSpacing : 0}`}>
				<img src={icon} alt="" aria-hidden="true" />
			</div>
		{/if}

		<!-- Content from parent component -->
		<span class="slot-content"></span>
	{/if}
</button>

<style>
	.metallic-button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border: 1px solid;
		border-radius: 10px;
		cursor: pointer;
		font-weight: 600;
		letter-spacing: 0.025em;
		transition:
			box-shadow 0.2s ease,
			background 0.2s ease,
			border-color 0.2s ease;
		position: relative;
		text-align: center;
		outline: none;
		min-width: 2.5em;
		min-height: 2.5em;
	}

	.full-width {
		width: 100%;
	}

	/* Size variants */
	.small {
		padding: 8px 16px;
		font-size: 1rem;
	}

	.medium {
		padding: 12px 20px;
		font-size: 1.2rem;
	}

	.large {
		padding: 14px 28px;
		font-size: 1.4rem;
	}

	/* Hover effects by variant */
	.blue:not(.disabled):not(.loading):hover,
	.dark:not(.disabled):not(.loading):hover,
	.ghost:not(.disabled):not(.loading):hover,
	.success:not(.disabled):not(.loading):hover,
	.danger:not(.disabled):not(.loading):hover {
		box-shadow:
			0 6px 15px rgba(26, 73, 173, 0.5),
			0 -2px 0 transparent;
	}

	.blue:not(.disabled):not(.loading):hover {
		background: linear-gradient(135deg, #264f94 0%, #7baafb 30%, #5584e1 60%, #3563cf 100%);
		border-color: white;
	}

	.dark:not(.disabled):not(.loading):hover {
		background: linear-gradient(
			135deg,
			rgba(80, 80, 80, 0.9) 0%,
			rgba(160, 160, 160, 0.9) 30%,
			rgba(120, 120, 120, 0.9) 60%,
			rgba(40, 40, 40, 0.9) 100%
		);
		border-color: rgba(255, 255, 255, 0.6);
	}

	.ghost:not(.disabled):not(.loading):hover {
		background: rgba(100, 100, 100, 0.8);
		color: white;
		border-color: rgba(255, 255, 255, 0.7);
	}

	.success:not(.disabled):not(.loading):hover {
		background: linear-gradient(135deg, #0d5e2f 0%, #34a05c 30%, #24904a 60%, #0f6f35 100%);
		border-color: white;
	}

	.danger:not(.disabled):not(.loading):hover {
		background: linear-gradient(135deg, #a50000 0%, #ef5350 30%, #d32f2f 60%, #9a0000 100%);
		border-color: white;
	}

	/* Active/pressed state */
	.blue:not(.disabled):not(.loading):active,
	.dark:not(.disabled):not(.loading):active,
	.ghost:not(.disabled):not(.loading):active,
	.success:not(.disabled):not(.loading):active,
	.danger:not(.disabled):not(.loading):active {
		box-shadow:
			0 2px 8px rgba(26, 73, 173, 0.4),
			0 1px 0 transparent;
		transform: translateY(1px);
	}

	.success:not(.disabled):not(.loading):active {
		background: linear-gradient(135deg, #07341a 0%, #206d3c 30%, #155c2a 60%, #093d20 100%);
		border-color: white;
	}

	.danger:not(.disabled):not(.loading):active {
		background: linear-gradient(135deg, #6d0000 0%, #b71c1c 30%, #8b0000 60%, #5d0000 100%);
		border-color: white;
	}

	/* Icon styling */
	.icon {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.small .icon img {
		width: 1.1rem;
		height: 1.1rem;
	}

	.medium .icon img {
		width: 1.3rem;
		height: 1.3rem;
	}

	.large .icon img {
		width: 1.6rem;
		height: 1.6rem;
	}

	/* Focus state for accessibility */
	.metallic-button:focus-visible {
		outline: 2px solid white;
		outline-offset: 3px;
	}

	/* Loading spinner */
	.spinner {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		position: absolute;
		top: 0;
		left: 0;
	}

	.spinner-svg {
		width: 1.5em;
		height: 1.5em;
		animation: spin 1.2s linear infinite;
	}

	.spinner-circle {
		stroke-dasharray: 60;
		stroke-dashoffset: 50;
		animation: dash 1.5s ease-in-out infinite;
		stroke-linecap: round;
	}

	@keyframes spin {
		100% {
			transform: rotate(360deg);
		}
	}

	@keyframes dash {
		0% {
			stroke-dashoffset: 60;
		}
		50% {
			stroke-dashoffset: 0;
		}
		100% {
			stroke-dashoffset: -60;
		}
	}

	/* When pressed (for toggle buttons) */
	.metallic-button[aria-pressed='true'] {
		box-shadow: 0 0 10px rgba(255, 255, 255, 0.3) inset;
		transform: scale(0.98);
	}

	/* Reduced motion preference support */
	@media (prefers-reduced-motion: reduce) {
		.metallic-button {
			transition: none !important;
		}

		.spinner-svg {
			animation-duration: 2s;
		}
	}

	/* High contrast mode support */
	@media screen and (forced-colors: active) {
		.metallic-button {
			border: 2px solid ButtonText;
			color: ButtonText;
			background: ButtonFace;
		}

		.metallic-button:hover,
		.metallic-button:focus {
			border-color: Highlight;
			color: Highlight;
		}

		.metallic-button:disabled {
			border-color: GrayText;
			color: GrayText;
		}
	}
</style>
