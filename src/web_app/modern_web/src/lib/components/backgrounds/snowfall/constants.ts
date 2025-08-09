// src/lib/components/backgrounds/snowfall/constants.ts

export const backgroundGradient = [
	{ stop: 0, color: '#1a1a2e' },
	{ stop: 0.5, color: '#16213e' },
	{ stop: 1, color: '#0f3460' },
];

export const performanceThresholds = {
	minRenderFps: 30,
	lowPerformanceThreshold: 45,
	criticalPerformanceThreshold: 30,
};

export const qualitySettings = {
	high: {
		densityMultiplier: 1.0,
		enableShootingStars: true,
		enableSeasonal: true,
	},
	medium: {
		densityMultiplier: 0.75,
		enableShootingStars: true,
		enableSeasonal: true,
	},
	low: {
		densityMultiplier: 0.5,
		enableShootingStars: false,
		enableSeasonal: false,
	},
};

export const resizeConfig = {
	qualityRestoreDelay: 500,
	resizeQuality: 'low' as 'high' | 'medium' | 'low',
};
