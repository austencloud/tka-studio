function createSafePictographCopy(data) {
  if (!data) return null;
  try {
    const safeCopy = { ...data };
    safeCopy.redMotion = null;
    safeCopy.blueMotion = null;
    safeCopy.motions = [];
    if (safeCopy.redArrowData?.svgData) {
      const originalSvgData = safeCopy.redArrowData.svgData;
      safeCopy.redArrowData = {
        ...safeCopy.redArrowData,
        svgData: { ...originalSvgData }
      };
      if (safeCopy.redArrowData.svgData.element) {
        safeCopy.redArrowData.svgData.element = null;
      }
      if (safeCopy.redArrowData.svgData.paths) {
        safeCopy.redArrowData.svgData.paths = null;
      }
    }
    if (safeCopy.blueArrowData?.svgData) {
      const originalSvgData = safeCopy.blueArrowData.svgData;
      safeCopy.blueArrowData = {
        ...safeCopy.blueArrowData,
        svgData: { ...originalSvgData }
      };
      if (safeCopy.blueArrowData.svgData.element) {
        safeCopy.blueArrowData.svgData.element = null;
      }
      if (safeCopy.blueArrowData.svgData.paths) {
        safeCopy.blueArrowData.svgData.paths = null;
      }
    }
    if (safeCopy.gridData) {
      safeCopy.gridData = { ...safeCopy.gridData };
      if (safeCopy.gridData.element) {
        safeCopy.gridData.element = null;
      }
    }
    if (safeCopy.redPropData) {
      safeCopy.redPropData = { ...safeCopy.redPropData };
      if (safeCopy.redPropData.element) {
        safeCopy.redPropData.element = null;
      }
    }
    if (safeCopy.bluePropData) {
      safeCopy.bluePropData = { ...safeCopy.bluePropData };
      if (safeCopy.bluePropData.element) {
        safeCopy.bluePropData.element = null;
      }
    }
    return safeCopy;
  } catch (error) {
    console.error("Error creating safe pictograph copy:", error);
    return null;
  }
}
function createSafeBeatCopy(beat) {
  if (!beat) return null;
  try {
    const safeCopy = { ...beat };
    if (safeCopy.pictographData) {
      safeCopy.pictographData = createSafePictographCopy(safeCopy.pictographData);
    }
    return safeCopy;
  } catch (error) {
    console.error("Error creating safe beat copy:", error);
    return null;
  }
}
export {
  createSafeBeatCopy,
  createSafePictographCopy
};
