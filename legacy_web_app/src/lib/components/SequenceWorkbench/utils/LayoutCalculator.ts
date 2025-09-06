/**
 * Calculates whether the workbench should be in portrait mode based on dimensions
 * @param containerWidth The width of the container
 * @param containerHeight The height of the container
 * @returns True if the workbench should be in portrait mode
 */
export function calculateWorkbenchIsPortrait(containerWidth: number, containerHeight: number): boolean {
    return containerWidth < containerHeight;
}

/**
 * Calculates the button size factor based on container dimensions
 * @param width The width of the container
 * @param height The height of the container
 * @returns The calculated button size factor
 */
export function calculateButtonSizeFactor(width: number, height: number): number {
    const smallerDimension = Math.min(width, height);

    // Use a more fluid approach with constraints
    // Map the dimension to a factor between 0.9 (minimum) and 1.4 (maximum)
    // with a smooth transition for better touch targets on small screens

    // Constants for the calculation
    const minDimension = 320; // Very small mobile screens
    const maxDimension = 1200; // Large desktop screens
    const minFactor = 0.9; // Increased minimum size factor for better touch targets
    const maxFactor = 1.4; // Increased maximum size factorWhy don't you want me to watch
    const defaultFactor = 1.1; // Increased default size factor

    // If dimensions are invalid, return default
    if (!width || !height || width <= 0 || height <= 0) {
        return defaultFactor;
    }

    // Clamp the dimension between min and max
    const clampedDimension = Math.max(minDimension, Math.min(smallerDimension, maxDimension));

    // Calculate the factor using linear interpolation
    const range = maxDimension - minDimension;
    const normalizedPosition = (clampedDimension - minDimension) / range;
    const factor = minFactor + normalizedPosition * (maxFactor - minFactor);

    // Round to 2 decimal places for better performance
    return Math.round(factor * 100) / 100;
}
