// src/lib/state/image-export-settings.ts
import { browser } from '$app/environment';

export interface ImageExportSettings {
	// Export content options
	// includeStartPosition is now removed from user control - always true internally
	addUserInfo: boolean;
	addWord: boolean;
	addDifficultyLevel: boolean;
	addBeatNumbers: boolean;
	addReversalSymbols: boolean;

	// User information
	userName: string;
	customNote: string;

	// Directory preferences
	rememberLastSaveDirectory: boolean;
	lastSaveDirectory: string;

	// Category information for organizing exports
	useCategories: boolean;
	defaultCategory: string;
}

// Default settings - enable all enhancement features by default
export const defaultImageExportSettings: ImageExportSettings = {
	// Export content options
	// Start position is now always included
	addUserInfo: true,
	addWord: true,
	addDifficultyLevel: true,
	addBeatNumbers: true,
	addReversalSymbols: true,

	// User information
	userName: 'User',
	customNote: 'Created with The Kinetic Constructor',

	// Directory preferences
	rememberLastSaveDirectory: true,
	lastSaveDirectory: '',

	// Category information for organizing exports
	useCategories: true,
	defaultCategory: 'Sequences'
};

// Global state for image export settings
let imageExportState = $state(structuredClone(defaultImageExportSettings));

// Function to get the current settings
export function getImageExportSettings(): ImageExportSettings {
	return {
		// Start position is now always included
		addUserInfo: imageExportState.addUserInfo === true,
		addWord: imageExportState.addWord === true,
		addDifficultyLevel: imageExportState.addDifficultyLevel === true,
		addBeatNumbers: imageExportState.addBeatNumbers === true,
		addReversalSymbols: imageExportState.addReversalSymbols === true,
		userName: imageExportState.userName || defaultImageExportSettings.userName,
		customNote: imageExportState.customNote || defaultImageExportSettings.customNote,
		rememberLastSaveDirectory: imageExportState.rememberLastSaveDirectory === true,
		lastSaveDirectory: imageExportState.lastSaveDirectory || '',
		useCategories: imageExportState.useCategories === true,
		defaultCategory: imageExportState.defaultCategory || defaultImageExportSettings.defaultCategory
	};
}

// Function to update the settings
export function updateImageExportSettings(newSettings: Partial<ImageExportSettings>): void {
	const cleanSettings = {
		...imageExportState,
		...newSettings
	};

	cleanSettings.rememberLastSaveDirectory = cleanSettings.rememberLastSaveDirectory === true;
	// Start position is now always included
	cleanSettings.addUserInfo = cleanSettings.addUserInfo === true;
	cleanSettings.addWord = cleanSettings.addWord === true;
	cleanSettings.addDifficultyLevel = cleanSettings.addDifficultyLevel === true;
	cleanSettings.addBeatNumbers = cleanSettings.addBeatNumbers === true;
	cleanSettings.addReversalSymbols = cleanSettings.addReversalSymbols === true;
	cleanSettings.useCategories = cleanSettings.useCategories === true;

	imageExportState = cleanSettings;

	saveImageExportSettings();
}

// Load settings from localStorage
export function loadImageExportSettings(): void {
	try {
		if (!browser) return;

		const savedSettings = localStorage.getItem('image-export-settings');
		if (savedSettings) {
			try {
				const parsed = JSON.parse(savedSettings);

				if (!parsed || typeof parsed !== 'object') {
					throw new Error('Parsed settings is not an object');
				}

				const validatedSettings: Partial<ImageExportSettings> = {};

				// Start position is now always included
				validatedSettings.addUserInfo = parsed.addUserInfo === true;
				validatedSettings.addWord = parsed.addWord === true;
				validatedSettings.addDifficultyLevel = parsed.addDifficultyLevel === true;
				validatedSettings.addBeatNumbers = parsed.addBeatNumbers === true;
				validatedSettings.addReversalSymbols = parsed.addReversalSymbols === true;
				validatedSettings.rememberLastSaveDirectory = parsed.rememberLastSaveDirectory === true;
				validatedSettings.userName =
					typeof parsed.userName === 'string' && parsed.userName.trim() !== ''
						? parsed.userName
						: defaultImageExportSettings.userName;
				validatedSettings.customNote =
					typeof parsed.customNote === 'string'
						? parsed.customNote
						: defaultImageExportSettings.customNote;
				validatedSettings.lastSaveDirectory =
					typeof parsed.lastSaveDirectory === 'string'
						? parsed.lastSaveDirectory
						: defaultImageExportSettings.lastSaveDirectory;
				validatedSettings.useCategories = parsed.useCategories === true;
				validatedSettings.defaultCategory =
					typeof parsed.defaultCategory === 'string' && parsed.defaultCategory.trim() !== ''
						? parsed.defaultCategory
						: defaultImageExportSettings.defaultCategory;

				imageExportState = {
					...defaultImageExportSettings,
					...validatedSettings
				};
			} catch (parseError) {
				console.error('Failed to parse image export settings, using defaults', parseError);
				localStorage.removeItem('image-export-settings');
				imageExportState = structuredClone(defaultImageExportSettings);
			}
		}
	} catch (error) {
		console.error('Failed to load image export settings', error);
		imageExportState = structuredClone(defaultImageExportSettings);
	}
}

// Save settings to localStorage
export function saveImageExportSettings(): void {
	try {
		if (!browser) return;

		if (!imageExportState) {
			console.error('Cannot save image export settings: settings object is null or undefined');
			return;
		}

		const cleanSettings: ImageExportSettings = {
			// Start position is now always included
			addUserInfo: imageExportState.addUserInfo === true,
			addWord: imageExportState.addWord === true,
			addDifficultyLevel: imageExportState.addDifficultyLevel === true,
			addBeatNumbers: imageExportState.addBeatNumbers === true,
			addReversalSymbols: imageExportState.addReversalSymbols === true,
			userName: imageExportState.userName || defaultImageExportSettings.userName,
			customNote: imageExportState.customNote || defaultImageExportSettings.customNote,
			rememberLastSaveDirectory: imageExportState.rememberLastSaveDirectory === true,
			lastSaveDirectory: imageExportState.lastSaveDirectory || '',
			useCategories: imageExportState.useCategories === true,
			defaultCategory:
				imageExportState.defaultCategory || defaultImageExportSettings.defaultCategory
		};

		localStorage.setItem('image-export-settings', JSON.stringify(cleanSettings));
	} catch (error) {
		console.error('Failed to save image export settings', error);
	}
}
