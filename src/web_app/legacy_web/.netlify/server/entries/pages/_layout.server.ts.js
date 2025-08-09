let dataCache = null;
const load = async ({ fetch: eventFetch }) => {
  if (dataCache) {
    return {
      csvData: dataCache,
      error: null
    };
  }
  try {
    const diamondResponse = await eventFetch("/DiamondPictographDataframe.csv");
    const boxResponse = await eventFetch("/BoxPictographDataframe.csv");
    if (!diamondResponse.ok || !boxResponse.ok) {
      return {
        csvData: {
          diamondData: "",
          boxData: ""
        },
        error: "Failed to load pictograph data files."
      };
    }
    const diamondData = await diamondResponse.text();
    const boxData = await boxResponse.text();
    dataCache = { diamondData, boxData };
    return {
      csvData: dataCache,
      error: null
      // Indicate success
    };
  } catch (error) {
    return {
      csvData: {
        diamondData: "",
        boxData: ""
      },
      error: "An error occurred while loading pictograph data."
    };
  }
};
export {
  load
};
