/**
 * Application Initialization Service
 *
 * Handles the startup sequence and initialization of the application.
 * This service ensures all required services are ready before the app starts.
 */

import type {
	IApplicationInitializationService,
	IPersistenceService,
	ISettingsService,
} from '../interfaces';

export class ApplicationInitializationService implements IApplicationInitializationService {
	constructor(
		private settingsService: ISettingsService,
		private persistenceService: IPersistenceService
	) {}

	/**
	 * Initialize the application
	 */
	async initialize(): Promise<void> {
		try {
			console.log('🚀 Starting TKA V2 Modern initialization...');

			// Step 1: Load settings
			await this.initializeSettings();

			// Step 2: Initialize persistence layer
			await this.initializePersistence();

			// Step 3: Perform startup checks
			await this.performStartupChecks();

			// Step 4: Load initial data
			await this.loadInitialData();

			console.log('✅ TKA V2 Modern initialization complete');
		} catch (error) {
			console.error('❌ Application initialization failed:', error);
			throw new Error(
				`Initialization failed: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Initialize settings
	 */
	private async initializeSettings(): Promise<void> {
		try {
			console.log('⚙️ Loading application settings...');
			await this.settingsService.loadSettings();
			console.log('✅ Settings loaded successfully');
		} catch (error) {
			console.warn('⚠️ Failed to load settings, using defaults:', error);
			// Continue with default settings
		}
	}

	/**
	 * Initialize persistence layer
	 */
	private async initializePersistence(): Promise<void> {
		try {
			console.log('💾 Initializing persistence layer...');

			// Check localStorage availability
			if (typeof Storage === 'undefined') {
				throw new Error('LocalStorage is not available');
			}

			// Test localStorage
			const testKey = 'tka-v2-test';
			localStorage.setItem(testKey, 'test');
			localStorage.removeItem(testKey);

			console.log('✅ Persistence layer initialized');
		} catch (error) {
			console.error('❌ Persistence initialization failed:', error);
			throw new Error(
				`Persistence initialization failed: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Perform startup checks
	 */
	private async performStartupChecks(): Promise<void> {
		console.log('🔍 Performing startup checks...');

		// Check browser compatibility
		const checks = [
			this.checkSVGSupport(),
			this.checkES6Support(),
			this.checkLocalStorageSpace(),
		];

		const results = await Promise.allSettled(checks);
		const failures = results.filter((result) => result.status === 'rejected');

		if (failures.length > 0) {
			console.warn('⚠️ Some startup checks failed:', failures);
			// Continue anyway - these are warnings, not fatal errors
		}

		console.log('✅ Startup checks complete');
	}

	/**
	 * Load initial data
	 */
	private async loadInitialData(): Promise<void> {
		try {
			console.log('📂 Loading initial data...');

			// Load sequences count for info
			const sequences = await this.persistenceService.loadAllSequences();
			console.log(`📊 Found ${sequences.length} existing sequences`);

			console.log('✅ Initial data loaded');
		} catch (error) {
			console.warn('⚠️ Failed to load initial data:', error);
			// Continue - this is not fatal
		}
	}

	/**
	 * Check SVG support
	 */
	private async checkSVGSupport(): Promise<void> {
		if (!document.createElementNS) {
			throw new Error('SVG support not available');
		}

		const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
		if (!svg || typeof svg.createSVGRect !== 'function') {
			throw new Error('SVG functionality not fully supported');
		}
	}

	/**
	 * Check ES6 support
	 */
	private async checkES6Support(): Promise<void> {
		// Check for key ES6 features we use
		if (typeof Promise === 'undefined') {
			throw new Error('Promise support required');
		}

		if (typeof Map === 'undefined') {
			throw new Error('Map support required');
		}

		if (typeof Set === 'undefined') {
			throw new Error('Set support required');
		}
	}

	/**
	 * Check localStorage space
	 */
	private async checkLocalStorageSpace(): Promise<void> {
		try {
			// Try to store 1MB of data to test space
			const testData = 'x'.repeat(1024 * 1024); // 1MB
			const testKey = 'tka-v2-space-test';

			localStorage.setItem(testKey, testData);
			localStorage.removeItem(testKey);
		} catch {
			throw new Error('Insufficient localStorage space');
		}
	}

	/**
	 * Get initialization status
	 */
	getInitializationStatus(): {
		isInitialized: boolean;
		version: string;
		timestamp: string;
	} {
		return {
			isInitialized: true,
			version: '2.0.0',
			timestamp: new Date().toISOString(),
		};
	}
}
