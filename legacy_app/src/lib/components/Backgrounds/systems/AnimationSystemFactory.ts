import { createSnowflakeSystem } from './SnowflakeSystem';
import { createShootingStarSystem } from './ShootingStarSystem';
import { createSantaSystem } from './SantaSystem';
import type { AnimationSystem, Snowflake, ShootingStarState, SantaState } from '../types/types';

export const createAnimationSystem = <T>(
	type: 'snowflake' | 'shootingStar' | 'santa'
): AnimationSystem<T> => {
	switch (type) {
		case 'snowflake':
			return createSnowflakeSystem() as unknown as AnimationSystem<T>;
		case 'shootingStar':
			return createShootingStarSystem() as unknown as AnimationSystem<T>;
		case 'santa':
			return createSantaSystem() as unknown as AnimationSystem<T>;
		default:
			throw new Error(`Unknown animation system type: ${type}`);
	}
};

export const createAnimationSystems = (enableSeasonal: boolean = true) => {
	return {
		snowflake: createSnowflakeSystem(),
		shootingStar: createShootingStarSystem(),
		...(enableSeasonal ? { santa: createSantaSystem() } : {})
	};
};
