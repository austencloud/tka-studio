
// src/lib/components/common/utils/buttonUtils.ts
import { type ButtonState, type ButtonVariant, fallbackGradients, gradientTokens, colorTokens, borderTokens } from '../tokens/buttonTokens';

// Memoization utility
export function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map();

  return ((...args: any[]) => {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key);
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

export const computeButtonStyles = memoize((
  variant: ButtonVariant,
  state: ButtonState,
  isFullWidth: boolean,
  isRounded: boolean
): string => {
  // Determine appropriate style based on state and variant
  if (state === 'disabled') {
    if (variant === 'blue') {
      return `
        background: linear-gradient(
          135deg,
          rgba(30, 60, 114, 0.5) 0%,
          rgba(108, 156, 233, 0.5) 30%,
          rgba(74, 119, 212, 0.5) 60%,
          rgba(42, 82, 190, 0.5) 100%
        );
        color: ${colorTokens[variant].disabled};
        border-color: ${borderTokens[variant].disabled};
        pointer-events: none;
      `;
    } else {
      return `
        opacity: 0.6;
        color: ${colorTokens[variant].disabled};
        border-color: ${borderTokens[variant].disabled};
        ${fallbackGradients[variant].normal}
        pointer-events: none;
      `;
    }
  }

  if (state === 'loading') {
    return `
      ${gradientTokens[variant].loading || fallbackGradients[variant].loading}
      color: ${colorTokens[variant].normal};
      border-color: ${borderTokens[variant].normal};
      position: relative;
      overflow: hidden;
      pointer-events: none;
    `;
  }

  if (state === 'active') {
    return `
      ${gradientTokens[variant].active || fallbackGradients[variant].active}
      color: ${colorTokens[variant].active};
      border-color: ${borderTokens[variant].active};
      box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
    `;
  }

  // Normal state
  return `
    ${gradientTokens[variant].normal || fallbackGradients[variant].normal}
    color: ${colorTokens[variant].normal};
    border-color: ${borderTokens[variant].normal};
    width: ${isFullWidth ? '100%' : 'auto'};
    border-radius: ${isRounded ? '9999px' : 'var(--border-radius-md)'};
  `;
});
