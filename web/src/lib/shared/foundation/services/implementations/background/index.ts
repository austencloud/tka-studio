/**
 * Background Service Implementations
 *
 * ONLY implementation classes - NO interfaces re-exported here.
 */

// Core background services
export { BackgroundService } from "./BackgroundService";
export { BackgroundFactory } from "./BackgroundFactory";
export { BackgroundManager } from "./BackgroundManager";
export { PerformanceTracker } from "./PerformanceTracker";
export { ResourceTracker } from "./ResourceTracker";

// Background systems
export { AuroraBackgroundSystem } from "./systems/AuroraBackgroundSystem";
export { AuroraBorealisBackgroundSystem } from "./systems/AuroraBorealisBackgroundSystem";
export { BubblesBackgroundSystem } from "./systems/BubblesBackgroundSystem";
export { DeepOceanBackgroundSystem } from "./systems/DeepOceanBackgroundSystem";
export { NightSkyBackgroundSystem } from "./systems/NightSkyBackgroundSystem";
export { SnowfallBackgroundSystem } from "./systems/SnowfallBackgroundSystem";
export { StarfieldBackgroundSystem } from "./systems/StarfieldBackgroundSystem";

// Utility systems
export * from "./systems/ShootingStarSystem"; // Functions
export * from "./systems/SnowflakeSystem"; // Functions
