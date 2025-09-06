export interface CircleCoords {
    [key: string]: {
        hand_points: {
            normal: Record<string, { x: number; y: number }>;
            strict: Record<string, { x: number; y: number }>;
        };
        layer2_points: {
            normal: Record<string, { x: number; y: number }>;
            strict: Record<string, { x: number; y: number }>;
        };
        outer_points: Record<string, string>;
        center_point: { x: number; y: number };
    };
}
