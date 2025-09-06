export class MotionChecker {
    motion: any;

    constructor(motion: any) {
        this.motion = motion;
    }

    isShift(): boolean {
        return ['pro', 'anti', 'float'].includes(this.motion.motionType);
    }

    isDash(): boolean {
        return this.motion.motionType === 'dash';
    }

    isStatic(): boolean {
        return this.motion.motionType === 'static';
    }

    isFloat(): boolean {
        return this.motion.motionType === 'float';
    }

    isDashOrStatic(): boolean {
        return ['dash', 'static'].includes(this.motion.motionType);
    }
}
