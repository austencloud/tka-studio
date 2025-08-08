export const SERVICE_TOKENS = {
	ERROR_HANDLER: 'errorHandler',
	BACKGROUND_FACTORY: 'backgroundFactory',
	BACKGROUND_SERVICE: 'backgroundService',
	ID_GENERATOR: 'idGenerator',
	SVG_MANAGER: 'svgManager',
	SEQUENCE_DATA: 'sequenceData',
	PICTOGRAPH_DATA: 'pictographData',
	THEME_SERVICE: 'themeService',
	LOGGER: 'logger'
} as const;

export type ServiceToken = keyof typeof SERVICE_TOKENS;
