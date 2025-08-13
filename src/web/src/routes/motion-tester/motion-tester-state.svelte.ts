/**
 * Motion Tester State - Enhanced Dual Prop Version
 * 
 * Manages reactive state for testing individual or combined motions.
 * Supports independent control and visibility of blue and red props.
 */

import { 
	calculateStepEndpoints, 
	lerpAngle, 
	normalizeAnglePositive,
	normalizeAngleSigned,
	mapPositionToAngle,
	mapOrientationToAngle,
	type StepEndpoints,
	type PropAttributes 
} from '$lib/animator/utils/standalone-math.js';

import { 
	StandalonePortedEngine,
	type PropState
} from '$lib/animator';

export interface MotionTestParams {
	startLoc: string;
	endLoc: string;
	motionType: string;
	turns: number;
	propRotDir: string;
	startOri: string;
	endOri: string;
}

export interface PropVisibility {
	blue: boolean;
	red: boolean;
}

export interface AnimationTestState {
	progress: number;
	isPlaying: boolean;
	speed: number;
}

// Create a test sequence with separate blue and red parameters
function createDualPropTestSequence(blueParams: MotionTestParams, redParams: MotionTestParams) {
	// Create a simple 2-beat sequence for testing
	const testSequence = [
		// Metadata (index 0)
		{
			word: "DUAL_TEST",
			author: "Motion Tester",
			totalBeats: 1
		},
		// Start position (index 1)
		{
			beat: 0,
			letter: "START",
			letter_type: "start",
			blue_attributes: {
				start_loc: blueParams.startLoc,
				end_loc: blueParams.startLoc,
				start_ori: blueParams.startOri,
				end_ori: blueParams.startOri,
				motion_type: "static",
				prop_rot_dir: "cw",
				turns: 0
			},
			red_attributes: {
				start_loc: redParams.startLoc,
				end_loc: redParams.startLoc,
				start_ori: redParams.startOri,
				end_ori: redParams.startOri,
				motion_type: "static",
				prop_rot_dir: "cw",
				turns: 0
			}
		},
		// Target motion (index 2)
		{
			beat: 1,
			letter: "TEST",
			letter_type: "motion",
			blue_attributes: {
				start_loc: blueParams.startLoc,
				end_loc: blueParams.endLoc,
				start_ori: blueParams.startOri,
				end_ori: blueParams.endOri,
				motion_type: blueParams.motionType,
				prop_rot_dir: blueParams.propRotDir,
				turns: blueParams.turns
			},
			red_attributes: {
				start_loc: redParams.startLoc,
				end_loc: redParams.endLoc,
				start_ori: redParams.startOri,
				end_ori: redParams.endOri,
				motion_type: redParams.motionType,
				prop_rot_dir: redParams.propRotDir,
				turns: redParams.turns
			}
		}
	];
	
	return testSequence;
}

export function createMotionTesterState() {
	// Separate motion parameters for blue and red props
	let blueMotionParams = $state<MotionTestParams>({
		startLoc: 'n',
		endLoc: 'e',
		motionType: 'pro',
		turns: 0,
		propRotDir: 'cw',
		startOri: 'in',
		endOri: 'in'
	});

	let redMotionParams = $state<MotionTestParams>({
		startLoc: 's',
		endLoc: 'w', 
		motionType: 'pro',
		turns: 0,
		propRotDir: 'cw',
		startOri: 'in',
		endOri: 'in'
	});

	// Prop visibility controls
	let propVisibility = $state<PropVisibility>({
		blue: true,
		red: false  // Start with just blue visible for single prop testing
	});

	// Animation state
	let animationState = $state<AnimationTestState>({
		progress: 0,
		isPlaying: false,
		speed: 0.01
	});
	
	// Animation engine instance
	let animationEngine = new StandalonePortedEngine();
	let totalBeats = $state(1);
	let isEngineInitialized = $state(false);

	// Initialize engine when motion parameters change
	$effect(() => {
		const testSequence = createDualPropTestSequence(blueMotionParams, redMotionParams);
		if (animationEngine.initialize(testSequence)) {
			const metadata = animationEngine.getMetadata();
			totalBeats = metadata.totalBeats;
			isEngineInitialized = true;
			
			// Reset animation progress
			animationState.progress = 0;
			
			console.log('🎯 Dual prop motion tester engine initialized:', {
				blueMotion: blueMotionParams,
				redMotion: redMotionParams,
				visibility: propVisibility,
				totalBeats,
				metadata
			});
		} else {
			isEngineInitialized = false;
			console.error('❌ Failed to initialize dual prop motion tester engine');
		}
	});

	// Calculate current prop states from engine
	let currentPropStates = $derived(() => {
		if (!isEngineInitialized) {
			return {
				blue: { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 },
				red: { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 }
			};
		}
		
		// Calculate state for current progress
		const currentBeat = animationState.progress * totalBeats;
		animationEngine.calculateState(currentBeat);
		
		return {
			blue: animationEngine.getBluePropState(),
			red: animationEngine.getRedPropState()
		};
	});

	// Motion descriptions (derived)
	let blueMotionDescription = $derived(() => {
		return `Blue: ${blueMotionParams.startLoc.toUpperCase()} → ${blueMotionParams.endLoc.toUpperCase()} (${blueMotionParams.motionType}, ${blueMotionParams.turns} turns, ${blueMotionParams.propRotDir.toUpperCase()})`;
	});

	let redMotionDescription = $derived(() => {
		return `Red: ${redMotionParams.startLoc.toUpperCase()} → ${redMotionParams.endLoc.toUpperCase()} (${redMotionParams.motionType}, ${redMotionParams.turns} turns, ${redMotionParams.propRotDir.toUpperCase()})`;
	});

	// Animation frame management
	let animationFrameId: number | null = null;

	// Animation control functions
	function startAnimation() {
		animationState.isPlaying = true;
		animate();
	}

	function pauseAnimation() {
		animationState.isPlaying = false;
		if (animationFrameId) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}
	}

	function resetAnimation() {
		pauseAnimation();
		animationState.progress = 0;
	}

	function stepAnimation() {
		animationState.progress = Math.min(1, animationState.progress + 0.1);
	}

	function animate() {
		if (!animationState.isPlaying) return;
		
		animationState.progress += animationState.speed;
		if (animationState.progress > 1) {
			animationState.progress = 0;
		}
		
		animationFrameId = requestAnimationFrame(animate);
	}

	// Parameter update functions
	function updateBlueMotionParam<K extends keyof MotionTestParams>(
		key: K, 
		value: MotionTestParams[K]
	) {
		blueMotionParams[key] = value;
	}

	function updateRedMotionParam<K extends keyof MotionTestParams>(
		key: K, 
		value: MotionTestParams[K]
	) {
		redMotionParams[key] = value;
	}

	function setProgress(progress: number) {
		animationState.progress = Math.max(0, Math.min(1, progress));
	}

	function setSpeed(speed: number) {
		animationState.speed = Math.max(0.001, Math.min(0.1, speed));
	}

	// Visibility control functions
	function toggleBlueProp() {
		propVisibility.blue = !propVisibility.blue;
	}

	function toggleRedProp() {
		propVisibility.red = !propVisibility.red;
	}

	function setBluePropVisible(visible: boolean) {
		propVisibility.blue = visible;
	}

	function setRedPropVisible(visible: boolean) {
		propVisibility.red = visible;
	}

	function showBothProps() {
		propVisibility.blue = true;
		propVisibility.red = true;
	}

	function showOnlyBlue() {
		propVisibility.blue = true;
		propVisibility.red = false;
	}

	function showOnlyRed() {
		propVisibility.blue = false;
		propVisibility.red = true;
	}

	// Location update convenience functions
	function setBlueStartLocation(location: string) {
		updateBlueMotionParam('startLoc', location);
	}

	function setBlueEndLocation(location: string) {
		updateBlueMotionParam('endLoc', location);
	}

	function setRedStartLocation(location: string) {
		updateRedMotionParam('startLoc', location);
	}

	function setRedEndLocation(location: string) {
		updateRedMotionParam('endLoc', location);
	}

	// Debug calculations (derived) - Updated for dual prop approach
	let debugInfo = $derived(() => {
		if (!isEngineInitialized) return null;

		// Calculate endpoints for both props
		const blueStepDef = {
			blue_attributes: blueMotionParams as PropAttributes
		};
		const redStepDef = {
			red_attributes: redMotionParams as PropAttributes  
		};

		const blueEndpoints = calculateStepEndpoints(blueStepDef, 'blue');
		const redEndpoints = calculateStepEndpoints(redStepDef, 'red');
		
		if (!blueEndpoints || !redEndpoints) return null;

		const blueDeltaAngle = normalizeAngleSigned(
			blueEndpoints.targetCenterAngle - blueEndpoints.startCenterAngle
		);
		const redDeltaAngle = normalizeAngleSigned(
			redEndpoints.targetCenterAngle - redEndpoints.startCenterAngle
		);

		const blueTurnAngle = Math.PI * blueMotionParams.turns;
		const redTurnAngle = Math.PI * redMotionParams.turns;

		const blueDistance = Math.abs(blueDeltaAngle) * 180 / Math.PI;
		const redDistance = Math.abs(redDeltaAngle) * 180 / Math.PI;

		return {
			blue: {
				startCenterAngle: blueEndpoints.startCenterAngle,
				startStaffAngle: blueEndpoints.startStaffAngle,
				targetCenterAngle: blueEndpoints.targetCenterAngle,
				targetStaffAngle: blueEndpoints.targetStaffAngle,
				deltaAngle: blueDeltaAngle,
				turnAngle: blueTurnAngle,
				distance: blueDistance
			},
			red: {
				startCenterAngle: redEndpoints.startCenterAngle,
				startStaffAngle: redEndpoints.startStaffAngle,
				targetCenterAngle: redEndpoints.targetCenterAngle,
				targetStaffAngle: redEndpoints.targetStaffAngle,
				deltaAngle: redDeltaAngle,
				turnAngle: redTurnAngle,
				distance: redDistance
			},
			interpolationT: animationState.progress,
			currentBeat: animationState.progress * totalBeats
		};
	});

	// Orientation arrows for display
	function getOrientationArrow(orientation: string): string {
		const arrows: Record<string, string> = {
			'in': '→',
			'out': '←',
			'n': '↑',
			'e': '→',
			's': '↓',
			'w': '←',
			'clock': '↻',
			'counter': '↺'
		};
		return arrows[orientation] || '→';
	}

	// Cleanup on destroy
	function destroy() {
		pauseAnimation();
	}

	// Return the reactive state and methods
	return {
		// Reactive state (getters)
		get blueMotionParams() { return blueMotionParams; },
		get redMotionParams() { return redMotionParams; },
		get propVisibility() { return propVisibility; },
		get animationState() { return animationState; },
		get currentPropStates() { return currentPropStates; },
		get blueMotionDescription() { return blueMotionDescription; },
		get redMotionDescription() { return redMotionDescription; },
		get debugInfo() { return debugInfo; },
		get isEngineInitialized() { return isEngineInitialized; },
		get totalBeats() { return totalBeats; },

		// Motion parameter actions
		updateBlueMotionParam,
		updateRedMotionParam,
		setBlueStartLocation,
		setBlueEndLocation,
		setRedStartLocation,
		setRedEndLocation,

		// Animation actions
		setProgress,
		setSpeed,
		startAnimation,
		pauseAnimation,
		resetAnimation,
		stepAnimation,

		// Visibility actions
		toggleBlueProp,
		toggleRedProp,
		setBluePropVisible,
		setRedPropVisible,
		showBothProps,
		showOnlyBlue,
		showOnlyRed,

		// Utility actions
		getOrientationArrow,
		destroy
	};
}

export type MotionTesterState = ReturnType<typeof createMotionTesterState>;
