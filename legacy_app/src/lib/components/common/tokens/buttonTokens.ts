// src/lib/components/common/tokens/buttonTokens.ts
export type ButtonSize = 'small' | 'medium' | 'large';
export type ButtonVariant = 'blue' | 'dark' | 'ghost' | 'success' | 'danger';
export type ButtonState = 'normal' | 'active' | 'disabled' | 'loading';
export type IconPosition = 'left' | 'right' | 'only';

export interface SizeTokens {
	padding: string;
	fontSize: string;
	iconSize: string;
	borderRadius: string;
	height: string;
}

export interface ColorTokens {
	normal: string;
	hover: string;
	active: string;
	disabled: string;
}

// Modern approach using CSS custom properties
export const sizeTokens: Record<ButtonSize, SizeTokens> = {
	small: {
		padding: 'var(--spacing-3) var(--spacing-4)',
		fontSize: 'var(--font-size-sm)',
		iconSize: 'var(--icon-size-sm)',
		borderRadius: 'var(--border-radius-md)',
		height: 'var(--height-button-sm)'
	},
	medium: {
		padding: 'var(--spacing-4) var(--spacing-5)',
		fontSize: 'var(--font-size-md)',
		iconSize: 'var(--icon-size-md)',
		borderRadius: 'var(--border-radius-md)',
		height: 'var(--height-button-md)'
	},
	large: {
		padding: 'var(--spacing-4) var(--spacing-6)',
		fontSize: 'var(--font-size-lg)',
		iconSize: 'var(--icon-size-lg)',
		borderRadius: 'var(--border-radius-lg)',
		height: 'var(--height-button-lg)'
	}
};

export const colorTokens: Record<ButtonVariant, ColorTokens> = {
	blue: {
		normal: 'var(--color-text-on-primary)',
		hover: 'var(--color-text-on-primary)',
		active: 'var(--color-text-on-primary)',
		disabled: 'var(--color-text-disabled)'
	},
	dark: {
		normal: 'var(--color-text-on-dark)',
		hover: 'var(--color-text-on-dark)',
		active: 'var(--color-text-on-dark)',
		disabled: 'var(--color-text-disabled-dark)'
	},
	ghost: {
		normal: 'var(--color-text-on-dark)',
		hover: 'var(--color-text-on-dark)',
		active: 'var(--color-text-on-dark)',
		disabled: 'var(--color-text-disabled-dark)'
	},
	success: {
		normal: 'var(--color-text-on-success)',
		hover: 'var(--color-text-on-success)',
		active: 'var(--color-text-on-success)',
		disabled: 'var(--color-text-disabled)'
	},
	danger: {
		normal: 'var(--color-text-on-danger)',
		hover: 'var(--color-text-on-danger)',
		active: 'var(--color-text-on-danger)',
		disabled: 'var(--color-text-disabled)'
	}
};

export const borderTokens: Record<ButtonVariant, ColorTokens> = {
	blue: {
		normal: 'var(--color-border-primary-light)',
		hover: 'var(--color-border-primary-lighter)',
		active: 'var(--color-border-primary-lighter)',
		disabled: 'var(--color-border-disabled)'
	},
	dark: {
		normal: 'var(--color-border-dark-light)',
		hover: 'var(--color-border-dark-lighter)',
		active: 'var(--color-border-dark-lighter)',
		disabled: 'var(--color-border-dark-disabled)'
	},
	ghost: {
		normal: 'var(--color-border-ghost)',
		hover: 'var(--color-border-ghost-hover)',
		active: 'var(--color-border-ghost-active)',
		disabled: 'var(--color-border-disabled)'
	},
	success: {
		normal: 'var(--color-border-success)',
		hover: 'var(--color-border-success-hover)',
		active: 'var(--color-border-success-active)',
		disabled: 'var(--color-border-disabled)'
	},
	danger: {
		normal: 'var(--color-border-danger)',
		hover: 'var(--color-border-danger-hover)',
		active: 'var(--color-border-danger-active)',
		disabled: 'var(--color-border-disabled)'
	}
};

// Gradients stored as CSS variables that can be defined in a global stylesheet
export const gradientTokens: Record<ButtonVariant, Record<string, string>> = {
	blue: {
		normal: 'var(--gradient-blue-normal)',
		hover: 'var(--gradient-blue-hover)',
		active: 'var(--gradient-blue-active)',
		loading: 'var(--gradient-blue-loading)'
	},
	dark: {
		normal: 'var(--gradient-dark-normal)',
		hover: 'var(--gradient-dark-hover)',
		active: 'var(--gradient-dark-active)',
		loading: 'var(--gradient-dark-loading)'
	},
	ghost: {
		normal: 'var(--gradient-ghost-normal)',
		hover: 'var(--gradient-ghost-hover)',
		active: 'var(--gradient-ghost-active)',
		loading: 'var(--gradient-ghost-loading)'
	},
	success: {
		normal: 'var(--gradient-success-normal)',
		hover: 'var(--gradient-success-hover)',
		active: 'var(--gradient-success-active)',
		loading: 'var(--gradient-success-loading)'
	},
	danger: {
		normal: 'var(--gradient-danger-normal)',
		hover: 'var(--gradient-danger-hover)',
		active: 'var(--gradient-danger-active)',
		loading: 'var(--gradient-danger-loading)'
	}
};

// Fallback gradient values if CSS variables are not set
export const fallbackGradients = {
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
    `,
		loading: `
      background: linear-gradient(
        135deg,
        #1e3c72 0%,
        #6c9ce9 30%,
        #4a77d4 60%,
        #2a52be 100%
      );
    `
	},
	dark: {
		normal: `
      background: linear-gradient(
        135deg,
        rgba(40, 40, 40, 0.9) 0%,
        rgba(55, 55, 55, 0.9) 50%,
        rgba(70, 70, 70, 0.9) 100%
      );
    `,
		hover: `
      background: linear-gradient(
        135deg,
        rgba(80, 80, 80, 0.9) 0%,
        rgba(160, 160, 160, 0.9) 30%,
        rgba(120, 120, 120, 0.9) 60%,
        rgba(40, 40, 40, 0.9) 100%
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
    `,
		loading: `
      background: linear-gradient(
        135deg,
        rgba(40, 40, 40, 0.9) 0%,
        rgba(55, 55, 55, 0.9) 50%,
        rgba(70, 70, 70, 0.9) 100%
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
    `,
		loading: `
      background: rgba(70, 70, 70, 0.7);
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
    `,
		loading: `
      background: linear-gradient(
        135deg,
        #0b4d26 0%,
        #2e8c50 30%,
        #1f7a3d 60%,
        #0d5e2f 100%
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
    `,
		loading: `
      background: linear-gradient(
        135deg,
        #8b0000 0%,
        #d32f2f 30%,
        #b71c1c 60%,
        #7f0000 100%
      );
    `
	}
};
