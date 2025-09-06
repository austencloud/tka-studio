// src/lib/components/objects/Prop/PropData.ts
import type { Color, Loc, Orientation, PropType, RadialMode } from '$lib/types/Types';

export interface PropData {
	id: string;
	motionId?: string; // Optional parent reference
	propType: PropType;
	color: Color;
	radialMode: RadialMode;
	ori: Orientation;
	coords: { x: number; y: number };
	loc: Loc;
	rotAngle: number;
	svgCenter?: { x: number; y: number }; // Optional SVG center
}

// You can also create a type guard to check if a PropData object is fully initialized
export function isValidPropData(prop: any): prop is PropData {
	return (
		prop &&
		typeof prop.id === 'string' &&
		typeof prop.propType !== 'undefined' &&
		typeof prop.color !== 'undefined' &&
		typeof prop.radialMode !== 'undefined' &&
		typeof prop.ori !== 'undefined' &&
		typeof prop.coords === 'object' &&
		typeof prop.coords.x === 'number' &&
		typeof prop.coords.y === 'number' &&
		typeof prop.loc !== 'undefined' &&
		typeof prop.rotAngle === 'number'
	);
}
