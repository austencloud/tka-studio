// src/lib/components/Backgrounds/deepOcean/OceanConfiguration.ts

import type { QualityLevel } from '../types/types';

export interface OceanConfig {
	background: {
		gradientStops: Array<{ position: number; color: string }>;
	};
	particles: {
		density: number;
		bubbleColors: string[];
		planktonColors: string[];
		debrisColors: string[];
	};
	jellyfish: {
		count: Record<QualityLevel, number>;
		colors: string[];
	};
	fish: {
		schoolSize: Record<QualityLevel, number>;
		schoolCount: Record<QualityLevel, number>;
		colors: string[];
	};
	coral: {
		count: Record<QualityLevel, number>;
		colors: string[];
	};
	whale: {
		size: number;
		speed: number;
		color: string;
	};
}

export class OceanConfiguration {
	private static instance: OceanConfiguration;

	private readonly config: OceanConfig = {
		background: {
			gradientStops: [
				{ position: 0, color: '#001122' },
				{ position: 0.3, color: '#003366' },
				{ position: 0.7, color: '#004080' },
				{ position: 1, color: '#001133' }
			]
		},
		particles: {
			density: 0.00008,
			bubbleColors: ['rgba(255,255,255,0.6)', 'rgba(173,216,230,0.4)', 'rgba(135,206,235,0.3)'],
			planktonColors: ['rgba(0,255,127,0.8)', 'rgba(50,205,50,0.6)', 'rgba(144,238,144,0.4)'],
			debrisColors: ['rgba(139,69,19,0.3)', 'rgba(160,82,45,0.2)', 'rgba(205,133,63,0.1)']
		},
		jellyfish: {
			count: { high: 3, medium: 2, low: 1, minimal: 0 },
			colors: [
				'rgba(255,20,147,0.7)',
				'rgba(138,43,226,0.6)',
				'rgba(75,0,130,0.5)',
				'rgba(0,191,255,0.6)'
			]
		},
		fish: {
			schoolSize: { high: 12, medium: 8, low: 4, minimal: 2 },
			schoolCount: { high: 3, medium: 2, low: 1, minimal: 1 },
			colors: ['#FFD700', '#FF6347', '#32CD32', '#1E90FF', '#FF69B4']
		},
		coral: {
			count: { high: 4, medium: 3, low: 2, minimal: 1 },
			colors: ['#FF7F50', '#FF6347', '#FF1493', '#DA70D6', '#9370DB']
		},
		whale: {
			size: 120,
			speed: 0.0008,
			color: '#2F4F4F'
		}
	};

	public static getInstance(): OceanConfiguration {
		if (!OceanConfiguration.instance) {
			OceanConfiguration.instance = new OceanConfiguration();
		}
		return OceanConfiguration.instance;
	}

	public getConfig(): OceanConfig {
		return this.config;
	}

	public getParticleCount(
		quality: QualityLevel,
		dimensions: { width: number; height: number }
	): number {
		const baseCount = Math.floor(
			dimensions.width * dimensions.height * this.config.particles.density
		);
		const qualityMultiplier =
			quality === 'high' ? 1 : quality === 'medium' ? 0.7 : quality === 'low' ? 0.4 : 0.2;
		return Math.floor(baseCount * qualityMultiplier);
	}

	public getJellyfishCount(quality: QualityLevel): number {
		return this.config.jellyfish.count[quality];
	}

	public getFishSchoolSize(quality: QualityLevel): number {
		return this.config.fish.schoolSize[quality];
	}

	public getFishSchoolCount(quality: QualityLevel): number {
		return this.config.fish.schoolCount[quality];
	}

	public getCoralCount(quality: QualityLevel): number {
		return this.config.coral.count[quality];
	}
}
