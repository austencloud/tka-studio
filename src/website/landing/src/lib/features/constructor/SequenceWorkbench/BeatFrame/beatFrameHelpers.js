// Beat frame helpers
export function autoAdjustLayout(container, beats) {
  return { rows: 2, cols: 4 };
}

export function calculateCellSize(containerWidth, containerHeight, rows, cols) {
  return Math.min(containerWidth / cols, containerHeight / rows) - 10;
}