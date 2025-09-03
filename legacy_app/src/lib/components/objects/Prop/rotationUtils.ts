export function rotateOffset(point: { x: number; y: number }, angleDeg: number) {
	const angleRad = (angleDeg * Math.PI) / 180;
	return {
		x: point.x * Math.cos(angleRad) - point.y * Math.sin(angleRad),
		y: point.x * Math.sin(angleRad) + point.y * Math.cos(angleRad)
	};
}
;
