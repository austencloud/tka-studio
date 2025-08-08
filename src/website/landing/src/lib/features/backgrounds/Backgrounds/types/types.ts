// src/lib/components/Backgrounds/types/types.ts
// Background types
export type BackgroundType = 'snowfall' | 'nightSky' | 'deepOcean';

// --- Other type definitions remain the same ---
export interface ParallaxLayer {
	stars: Star[];
	driftX: number;
	driftY: number;
}

export type Dimensions = {
	width: number;
	height: number;
};

export type PerformanceMetrics = {
	fps: number;
	warnings: string[];
	particleCount?: number;
	renderTime?: number;
	memoryUsage?: number;
};

export type QualityLevel = 'high' | 'medium' | 'low' | 'minimal';

export interface GradientStop {
	position: number;
	color: string;
}

export interface QualitySettings {
	densityMultiplier: number;
	enableShootingStars: boolean;
	enableSeasonal: boolean; // Can be repurposed for other effects
	particleComplexity: 'high' | 'medium' | 'low' | 'minimal';
	enableBloom: boolean;
	enableReflections: boolean; // Can be repurposed
}

export interface AccessibilitySettings {
	reducedMotion: boolean;
	highContrast: boolean;
	visibleParticleSize: number;
}

export interface AnimationComponent {
	initialize: (dimensions: Dimensions, quality: QualityLevel) => void;
	update: (dimensions: Dimensions) => void;
	draw: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
	cleanup: () => void;
	setQuality: (quality: QualityLevel) => void;
	setAccessibility?: (settings: AccessibilitySettings) => void;
}

// --- Snowfall specific types (keep for now) ---
export interface Snowflake {
	x: number;
	y: number;
	speed: number;
	size: number;
	sway: number;
	opacity: number;
	shape: Path2D;
	color: string;
}

export interface ShootingStar {
	x: number;
	y: number;
	dx: number;
	dy: number;
	size: number;
	speed: number;
	tail: Array<{
		x: number;
		y: number;
		size: number;
		color: string;
	}>;
	prevX: number;
	prevY: number;
	tailLength: number;
	opacity: number;
	offScreen: boolean;
	color: string;
	twinkle: boolean;
}

export interface ShootingStarState {
	star: ShootingStar | null;
	timer: number;
	interval: number;
}

export interface SantaState {
	x: number;
	y: number;
	speed: number;
	active: boolean;
	direction: number;
	opacity: number;
	imageLoaded?: boolean;
}
// --- End Snowfall specific types ---

// --- Night Sky specific types (NEW) ---
export interface Star {
	x: number;
	y: number;
	radius: number;
	baseOpacity: number;
	currentOpacity: number;
	twinkleSpeed: number;
	twinklePhase: number; // To offset sin wave
	isTwinkling: boolean;
	color: string;
}

export interface CelestialBody {
	x: number;
	y: number;
	radius: number;
	color: string; // This will be the illuminated color of the moon
	driftX?: number;
	driftY?: number;
	// NEW: Moon phase specific properties
	illumination?: {
		fraction: number; // Illuminated fraction (0.0 to 1.0)
		phaseValue: number; // Moon phase (0=new, 0.25=1st Q, 0.5=full, 0.75=3rd Q, 1=new again)
		angle: number; // Angle of the moon's bright limb (from SunCalc)
	};
}

export interface Spaceship {
	x: number;
	y: number;
	width: number;
	height: number;
	speed: number;
	active: boolean;
	direction: number; // 1 for right, -1 for left
	opacity: number;
	image?: HTMLImageElement; // Optional image
	imageLoaded?: boolean;
}

export interface EasterEggState<T> {
	element: T | null;
	timer: number;
	interval: number;
}
// --- End Night Sky specific types ---

export interface AnimationSystem<T> {
	initialize: (dimensions: Dimensions, quality: QualityLevel) => T;
	update: (state: T, dimensions: Dimensions) => T;
	draw: (state: T, ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
	cleanup?: () => void;
	setQuality?: (quality: QualityLevel) => void;
	adjustToResize?: (
		state: T,
		oldDimensions: Dimensions,
		newDimensions: Dimensions,
		quality: QualityLevel
	) => T;
	setAccessibility?: (settings: AccessibilitySettings) => void;
}

export interface BackgroundSystem {
	initialize: (dimensions: Dimensions, quality: QualityLevel) => void;
	update: (dimensions: Dimensions) => void;
	draw: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void;
	setQuality: (quality: QualityLevel) => void;
	cleanup: () => void;
	handleResize?: (oldDimensions: Dimensions, newDimensions: Dimensions) => void;
	setAccessibility?: (settings: AccessibilitySettings) => void;
	getMetrics?: () => PerformanceMetrics;
}

export interface BackgroundFactoryParams {
	type: BackgroundType;
	initialQuality?: QualityLevel;
	accessibility?: AccessibilitySettings;
	customConfig?: any;
}

export type BackgroundEvent =
	| { type: 'ready' }
	| { type: 'performanceReport'; metrics: PerformanceMetrics }
	| { type: 'qualityChanged'; quality: QualityLevel }
	| { type: 'error'; message: string; stack?: string };

export interface ResourceTracker {
	trackResource: (resource: any) => void;
	untrackResource: (resource: any) => void;
	disposeAll: () => void;
}
