// Background Services Registration
import type { ServiceContainer } from "../ServiceContainer";
import { IBackgroundServiceInterface } from "../interfaces/background-interfaces";

export async function registerBackgroundServices(
  container: ServiceContainer
): Promise<void> {
  // Register background animation services
  container.register(IBackgroundServiceInterface);

  console.log("✅ Background services registered");
}
