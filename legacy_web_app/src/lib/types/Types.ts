export type VTGTiming = 'split' | 'tog';
export type VTGDir = 'same' | 'opp';
export type GridMode = 'diamond' | 'box';
export type DirRelation = 's' | 'o';
export type MotionType = 'anti' | 'pro' | 'static' | 'dash' | 'float';
export type ShiftMotionType = 'pro' | 'anti' | 'float';
export type PropRotDir = 'cw' | 'ccw' | 'no_rot';
export type TranslationDirection =
	| 'up'
	| 'down'
	| 'left'
	| 'right'
	| 'upright'
	| 'upleft'
	| 'downright'
	| 'downleft';
export type Color = 'blue' | 'red';
export type LeadState = 'leading' | 'trailing' | null;
export type HandRotDir = 'cw_shift' | 'ccw_shift' | 'dash' | 'static' | null;
export type ShiftHandRotDir = 'cw_shift' | 'ccw_shift';
export type Orientation = 'in' | 'out' | 'clock' | 'counter';
export type TKATurns = 'fl' | 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3;
export type RadialMode = 'radial' | 'nonradial';
export type DiamondLoc = 'n' | 's' | 'e' | 'w';
export type BoxLoc = 'ne' | 'se' | 'sw' | 'nw';
export type Loc = 'n' | 's' | 'e' | 'w' | 'ne' | 'se' | 'sw' | 'nw';
export enum PropType {
	HAND = 'hand',
	STAFF = 'staff',
	TRIAD = 'triad',
	MINIHOOP = 'minihoop',
	FAN = 'fan',
	CLUB = 'club',
	BUUGENG = 'buugeng'
}
export type Direction =
	| 'up'
	| 'down'
	| 'left'
	| 'right'
	| 'upright'
	| 'upleft'
	| 'downright'
	| 'downleft';
