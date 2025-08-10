/**
 * Application Bootstrap - TKA V2 Modern
 *
 * This module creates and configures the application's dependency injection container,
 * registering all services and their dependencies following the clean architecture
 * pattern established in the desktop application.
 */

import { ServiceContainer } from './di/ServiceContainer';
import type { ServiceInterface } from './di/types';
import { createServiceInterface } from './di/types';

// Import service interface types
import type {
	IApplicationInitializationService,
	IArrowPlacementDataService,
	IArrowPlacementKeyService,
	IArrowPositioningService,
	IConstructTabCoordinationService,
	IDeviceDetectionService,
	IExportService,
	IMotionGenerationService,
	IOptionDataService,
	IPersistenceService,
	IPictographRenderingService,
	IPictographService,
	IPropRenderingService,
	ISequenceDomainService,
	ISequenceGenerationService,
	ISequenceService,
	ISettingsService,
	IStartPositionService,
} from './interfaces.js';

// Import service implementations
import { ApplicationInitializationService } from './implementations/ApplicationInitializationService';
import { ArrowPlacementDataService } from './implementations/ArrowPlacementDataService';
import { ArrowPlacementKeyService } from './implementations/ArrowPlacementKeyService';
import { ArrowPositioningService } from './implementations/ArrowPositioningService';
import { ConstructTabCoordinationService } from './implementations/ConstructTabCoordinationService';
import { DeviceDetectionService } from './implementations/DeviceDetectionService';
import { ExportService } from './implementations/ExportService';
import { LocalStoragePersistenceService } from './implementations/LocalStoragePersistenceService';
import { MotionGenerationService } from './implementations/MotionGenerationService';
import { OptionDataService } from './implementations/OptionDataService';
import { PictographRenderingService } from './implementations/PictographRenderingService';
import { PictographService } from './implementations/PictographService';
import { PropRenderingService } from './implementations/PropRenderingService';
import { SequenceDomainService } from './implementations/SequenceDomainService';
import { SequenceGenerationService } from './implementations/SequenceGenerationService';
import { SequenceService } from './implementations/SequenceService';
import { SettingsService } from './implementations/SettingsService';
import { StartPositionService } from './implementations/StartPositionService';

// Create ServiceInterface objects for DI container
const ISequenceServiceInterface = createServiceInterface<ISequenceService>(
	'ISequenceService',
	SequenceService
);
const ISequenceDomainServiceInterface = createServiceInterface<ISequenceDomainService>(
	'ISequenceDomainService',
	SequenceDomainService
);
const IPictographServiceInterface = createServiceInterface<IPictographService>(
	'IPictographService',
	PictographService
);
const IPictographRenderingServiceInterface = createServiceInterface<IPictographRenderingService>(
	'IPictographRenderingService',
	PictographRenderingService
);
const IArrowPositioningServiceInterface = createServiceInterface<IArrowPositioningService>(
	'IArrowPositioningService',
	ArrowPositioningService
);
const IArrowPlacementDataServiceInterface = createServiceInterface<IArrowPlacementDataService>(
	'IArrowPlacementDataService',
	ArrowPlacementDataService
);
const IArrowPlacementKeyServiceInterface = createServiceInterface<IArrowPlacementKeyService>(
	'IArrowPlacementKeyService',
	ArrowPlacementKeyService
);
const IPropRenderingServiceInterface = createServiceInterface<IPropRenderingService>(
	'IPropRenderingService',
	PropRenderingService
);
const IPersistenceServiceInterface = createServiceInterface<IPersistenceService>(
	'IPersistenceService',
	LocalStoragePersistenceService
);
const ISequenceGenerationServiceInterface = createServiceInterface<ISequenceGenerationService>(
	'ISequenceGenerationService',
	SequenceGenerationService
);
const IMotionGenerationServiceInterface = createServiceInterface<IMotionGenerationService>(
	'IMotionGenerationService',
	MotionGenerationService
);
const IApplicationInitializationServiceInterface =
	createServiceInterface<IApplicationInitializationService>(
		'IApplicationInitializationService',
		ApplicationInitializationService
	);
const ISettingsServiceInterface = createServiceInterface<ISettingsService>(
	'ISettingsService',
	SettingsService
);
const IExportServiceInterface = createServiceInterface<IExportService>(
	'IExportService',
	ExportService
);
const IConstructTabCoordinationServiceInterface =
	createServiceInterface<IConstructTabCoordinationService>(
		'IConstructTabCoordinationService',
		ConstructTabCoordinationService
	);
const IOptionDataServiceInterface = createServiceInterface<IOptionDataService>(
	'IOptionDataService',
	OptionDataService
);
const IStartPositionServiceInterface = createServiceInterface<IStartPositionService>(
	'IStartPositionService',
	StartPositionService
);
const IDeviceDetectionServiceInterface = createServiceInterface<IDeviceDetectionService>(
	'IDeviceDetectionService',
	DeviceDetectionService
);

/**
 * Create and configure the web application DI container
 */
export async function createWebApplication(): Promise<ServiceContainer> {
	const container = new ServiceContainer('tka-web-v2');

	try {
		// Register domain services (no dependencies)
		container.registerSingletonClass(ISequenceDomainServiceInterface);

		// Register infrastructure services
		container.registerSingletonClass(IPersistenceServiceInterface);
		container.registerSingletonClass(ISettingsServiceInterface);
		container.registerSingletonClass(IDeviceDetectionServiceInterface);

		// Register placement services (no dependencies)
		container.registerSingletonClass(IArrowPlacementDataServiceInterface);
		container.registerSingletonClass(IArrowPlacementKeyServiceInterface);

		// Register construct tab services
		container.registerSingletonClass(IStartPositionServiceInterface);
		container.registerSingletonClass(IOptionDataServiceInterface);
		container.registerFactory(IConstructTabCoordinationServiceInterface, () => {
			const sequenceService = container.resolve(ISequenceServiceInterface);
			const startPositionService = container.resolve(IStartPositionServiceInterface);

			return new ConstructTabCoordinationService(sequenceService, startPositionService);
		});

		// Register rendering services
		container.registerSingletonClass(IPropRenderingServiceInterface);

		// Register ArrowPositioningService with dependencies
		container.registerFactory(IArrowPositioningServiceInterface, () => {
			const placementDataService = container.resolve(IArrowPlacementDataServiceInterface);
			const placementKeyService = container.resolve(IArrowPlacementKeyServiceInterface);
			return new ArrowPositioningService(placementDataService, placementKeyService);
		});

		// Register PictographRenderingService with dependencies
		container.registerFactory(IPictographRenderingServiceInterface, () => {
			const arrowPositioning = container.resolve(IArrowPositioningServiceInterface);
			const propRendering = container.resolve(IPropRenderingServiceInterface);
			return new PictographRenderingService(arrowPositioning, propRendering);
		});
		container.registerSingletonClass(IPictographServiceInterface);

		// Register application services (with dependencies)
		container.registerFactory(ISequenceServiceInterface, () => {
			const sequenceDomainService = container.resolve(ISequenceDomainServiceInterface);
			const persistenceService = container.resolve(IPersistenceServiceInterface);
			return new SequenceService(sequenceDomainService, persistenceService);
		});
		container.registerSingletonClass(IExportServiceInterface);

		// Register generation services
		container.registerSingletonClass(IMotionGenerationServiceInterface);
		container.registerSingletonClass(ISequenceGenerationServiceInterface);

		// Register application initialization service with factory
		container.registerFactory(IApplicationInitializationServiceInterface, () => {
			const settingsService = container.resolve(ISettingsServiceInterface);
			const persistenceService = container.resolve(IPersistenceServiceInterface);
			return new ApplicationInitializationService(settingsService, persistenceService);
		});

		// Validate all registrations can be resolved
		await validateContainerConfiguration(container);

		// Set as global container so resolve() function works
		setGlobalContainer(container);

		console.log('✅ TKA V2 Modern application container initialized successfully');
		return container;
	} catch (error) {
		console.error('❌ Failed to initialize application container:', error);
		throw new Error(
			`Application initialization failed: ${error instanceof Error ? error.message : 'Unknown error'}`
		);
	}
}

/**
 * Validate that all registered services can be resolved
 */
async function validateContainerConfiguration(container: ServiceContainer): Promise<void> {
	const servicesToValidate = [
		// Core services needed by MainApplication
		IPersistenceServiceInterface,
		ISettingsServiceInterface,
		IDeviceDetectionServiceInterface,
		ISequenceDomainServiceInterface,
		ISequenceServiceInterface,
		IApplicationInitializationServiceInterface,
	];

	for (const serviceInterface of servicesToValidate) {
		try {
			console.log(`🔍 Validating service: ${serviceInterface.token}`);
			const service = container.resolve(serviceInterface as any);
			if (!service) {
				throw new Error(`Service ${serviceInterface.token} resolved to null/undefined`);
			}
			console.log(`✅ Service validated: ${serviceInterface.token}`);
		} catch (error) {
			console.error(`❌ Failed to validate service: ${serviceInterface.token}`, error);
			throw new Error(
				`Failed to resolve ${serviceInterface.token}: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}
}

/**
 * Global container instance for use throughout the application
 */
let globalContainer: ServiceContainer | null = null;

/**
 * Get the global container instance
 */
export function getContainer(): ServiceContainer {
	if (!globalContainer) {
		throw new Error(
			'Application container not initialized. Call createWebApplication() first.'
		);
	}
	return globalContainer;
}

/**
 * Set the global container instance (used by bootstrap)
 */
export function setGlobalContainer(container: ServiceContainer): void {
	globalContainer = container;
}

// Service interface mapping for string-based resolution
const serviceInterfaceMap = new Map<string, ServiceInterface<any>>([
	['ISequenceService', ISequenceServiceInterface],
	['ISequenceDomainService', ISequenceDomainServiceInterface],
	['IPictographService', IPictographServiceInterface],
	['IPictographRenderingService', IPictographRenderingServiceInterface],
	['IArrowPositioningService', IArrowPositioningServiceInterface],
	['IArrowPlacementDataService', IArrowPlacementDataServiceInterface],
	['IArrowPlacementKeyService', IArrowPlacementKeyServiceInterface],
	['IPropRenderingService', IPropRenderingServiceInterface],
	['IPersistenceService', IPersistenceServiceInterface],
	['ISequenceGenerationService', ISequenceGenerationServiceInterface],
	['IMotionGenerationService', IMotionGenerationServiceInterface],
	['IApplicationInitializationService', IApplicationInitializationServiceInterface],
	['ISettingsService', ISettingsServiceInterface],
	['IExportService', IExportServiceInterface],
	['IConstructTabCoordinationService', IConstructTabCoordinationServiceInterface],
	['IOptionDataService', IOptionDataServiceInterface],
	['IStartPositionService', IStartPositionServiceInterface],
	['IDeviceDetectionService', IDeviceDetectionServiceInterface],
]);

/**
 * Helper function to resolve services from the global container
 */
export function resolve<T>(serviceInterface: ServiceInterface<T> | string): T {
	const container = getContainer();

	if (typeof serviceInterface === 'string') {
		// Legacy string-based resolution for backward compatibility
		const mappedInterface = serviceInterfaceMap.get(serviceInterface);
		if (!mappedInterface) {
			throw new Error(`Service interface not found for key: ${serviceInterface}`);
		}
		return container.resolve(mappedInterface);
	}

	return container.resolve(serviceInterface);
}
