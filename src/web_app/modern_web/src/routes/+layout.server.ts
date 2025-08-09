// src/routes/+layout.server.ts - Modern version based on legacy
import type { LayoutServerLoad } from "./$types";

// Add a cache flag to prevent duplicate fetches
let dataCache: { diamondData: string; boxData: string } | null = null;

export const load: LayoutServerLoad = async ({ fetch: eventFetch }) => {
  // Return cached data if available
  if (dataCache) {
    return {
      csvData: dataCache,
      error: null,
    };
  }

  // Fetch data silently without console logs (similar to legacy)
  try {
    console.log('🔄 Loading CSV data from server...');
    
    // Use the event.fetch provided by SvelteKit
    const diamondResponse = await eventFetch("/DiamondPictographDataframe.csv");
    const boxResponse = await eventFetch("/BoxPictographDataframe.csv");

    if (!diamondResponse.ok || !boxResponse.ok) {
      // Return empty strings or handle error appropriately for the UI
      return {
        csvData: {
          diamondData: "",
          boxData: "",
        },
        error: "Failed to load pictograph data files.",
      };
    }

    const diamondData = await diamondResponse.text();
    const boxData = await boxResponse.text();

    // Store in cache
    dataCache = { diamondData, boxData };

    console.log('✅ CSV data loaded successfully on server');
    console.log(`   Diamond CSV: ${diamondData.split('\n').length - 1} rows`);
    console.log(`   Box CSV: ${boxData.split('\n').length - 1} rows`);

    return {
      csvData: dataCache,
      error: null, // Indicate success
    };
  } catch (error) {
    console.error('❌ Error loading CSV data on server:', error);
    // Silent error handling
    return {
      csvData: {
        diamondData: "",
        boxData: "",
      },
      error: "An error occurred while loading pictograph data.",
    };
  }
};
