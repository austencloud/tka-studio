import { ServiceContainer } from './ServiceContainer.js';
import { SERVICE_TOKENS } from './ServiceTokens.js';
import { BackgroundFactory } from '../components/Backgrounds/core/BackgroundFactory.js';
import type { BackgroundSystemFactory } from '../core/services/BackgroundSystem.js';

// Import the injectable services to trigger registration
import '$lib/services/InjectableErrorHandlingService';
import '$lib/services/BackgroundServiceImpl';
import '$lib/services/IdGeneratorImpl';
import '$lib/services/InjectableLoggerService';

export function registerServices(container: ServiceContainer): void {
	// Register background factory as a static class implementing BackgroundSystemFactory
	container.register<BackgroundSystemFactory>(SERVICE_TOKENS.BACKGROUND_FACTORY, BackgroundFactory);

	// More service registrations will go here
}
