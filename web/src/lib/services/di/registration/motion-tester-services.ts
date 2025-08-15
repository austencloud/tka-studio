/**
 * Motion Tester Services Registration
 *
 * Registers all services related to the motion tester functionality
 * following the TKA DI container pattern.
 */

import type { ServiceContainer } from "../ServiceContainer";
import { IAnimatedPictographDataServiceInterface } from "../interfaces/motion-tester-interfaces";

/**
 * Register all motion tester services
 */
export async function registerMotionTesterServices(
  container: ServiceContainer
): Promise<void> {
  // Register AnimatedPictographDataService
  container.registerSingletonClass(IAnimatedPictographDataServiceInterface);

  console.log("✅ Motion tester services registered successfully");
}
