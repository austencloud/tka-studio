/**
 * SequenceLayoutCalculator.ts
 *
 * This utility provides functions for calculating layout properties for the SequenceWidget
 * and related components. It centralizes layout logic to ensure consistent behavior across
 * the refactored components.
 */

/**
 * Calculate whether the workbench should use portrait orientation
 * based on container dimensions
 *
 * @param width Container width
 * @param height Container height
 * @returns Whether to use portrait orientation
 */
export function calculateWorkbenchIsPortrait(width: number, height: number): boolean {
    // Use portrait mode when width is less than height and below a threshold
    return width < height && width < 768;
}

/**
 * Calculate the button size factor based on container dimensions
 *
 * @param width Container width
 * @param height Container height
 * @returns Button size factor (0-1)
 */
export function calculateButtonSizeFactor(width: number, height: number): number {
    // Base size on the smaller dimension
    const smallerDimension = Math.min(width, height);

    // Scale factor based on container size
    // Smaller containers get smaller buttons
    if (smallerDimension < 400) {
        return 0.7; // Smaller buttons for small screens
    } else if (smallerDimension < 600) {
        return 0.8; // Medium buttons for medium screens
    } else {
        return 1.0; // Full size buttons for large screens
    }
}

/**
 * Calculate if the beat frame should scroll based on its natural height
 * and available space
 *
 * @param beatFrameNaturalHeight Natural height of the beat frame
 * @param containerHeight Available container height
 * @param labelHeight Height of the label above the beat frame
 * @param verticalPadding Vertical padding of the container
 * @returns Whether the beat frame should scroll
 */
export function calculateBeatFrameShouldScroll(
    beatFrameNaturalHeight: number,
    containerHeight: number,
    labelHeight: number,
    verticalPadding: number = 20
): boolean {
    if (beatFrameNaturalHeight <= 0) {
        return false; // Default if natural height isn't reported yet
    }

    // Define padding for the beat-frame-wrapper that is outside the scrollable area
    const beatFrameWrapperPaddingBottom = 10;

    const availableHeightForBeatFrameAndLabel = containerHeight - verticalPadding;
    const availableHeightForBeatFrameItself =
        availableHeightForBeatFrameAndLabel - labelHeight - beatFrameWrapperPaddingBottom;

    // Should scroll if the natural height exceeds available space
    return beatFrameNaturalHeight > availableHeightForBeatFrameItself;
}

/**
 * Calculate the combined height of the label and beat frame unit
 *
 * @param labelHeight Height of the label
 * @param beatFrameHeight Height of the beat frame
 * @returns Combined height of the label and beat frame unit
 */
export function calculateCombinedUnitHeight(
    labelHeight: number,
    beatFrameHeight: number
): number {
    return labelHeight + beatFrameHeight;
}

/**
 * Calculate the available height for the beat frame
 *
 * @param containerHeight Total container height
 * @param labelHeight Height of the label
 * @param verticalPadding Vertical padding of the container
 * @returns Available height for the beat frame
 */
export function calculateAvailableHeightForBeatFrame(
    containerHeight: number,
    labelHeight: number,
    verticalPadding: number = 20
): number {
    const beatFrameWrapperPaddingBottom = 10;
    const availableHeightForBeatFrameAndLabel = containerHeight - verticalPadding;
    return availableHeightForBeatFrameAndLabel - labelHeight - beatFrameWrapperPaddingBottom;
}
