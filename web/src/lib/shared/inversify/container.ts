import { Container } from "inversify";
import {
  coreModule,
  animatorModule,
  browseModule,
  buildModule,
  exportModule,
  pictographModule,
  learnModule,
  wordCardModule,
  writeModule,
  dataModule
} from "./modules";

// Create container
const container = new Container();

// Load all modules
async function initializeContainer() {
  try {
    await container.load(
      coreModule,
      dataModule,
      pictographModule,
      animatorModule,
      browseModule,
      buildModule,
      exportModule,
      learnModule,
      wordCardModule,
      writeModule
    );
    console.log("✅ TKA Container: All modules loaded successfully");
  } catch (error) {
    console.error("❌ TKA Container: Failed to load modules:", error);
    throw error;
  }
}

// Initialize the container
initializeContainer();

// Export container
export { container };
export const inversifyContainer = container;

// Export TYPES for convenience (many files expect to import TYPES from container)
export { TYPES } from "./types";

// Export resolve function
export function resolve<T>(serviceType: symbol): T {
  return container.get<T>(serviceType);
}

// Export module initialization function for testing or manual control
export { initializeContainer };
