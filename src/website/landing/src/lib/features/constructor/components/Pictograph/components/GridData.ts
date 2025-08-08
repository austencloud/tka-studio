export interface GridData {
	allHandPointsStrict: Record<string, { coordinates: { x: number; y: number } | null }>;
	allHandPointsNormal: Record<string, { coordinates: { x: number; y: number } | null }>;
	allLayer2PointsStrict: Record<string, { coordinates: { x: number; y: number } | null }>;
	allLayer2PointsNormal: Record<string, { coordinates: { x: number; y: number } | null }>;
	allOuterPoints: Record<string, { coordinates: { x: number; y: number } | null }>;
	centerPoint: { coordinates: { x: number; y: number } | null };
}
