/**
 * Simple Arrow Positioning Service
 *
 * Temporary simplified version while we complete the full microservices integration.
 * This provides basic positioning functionality to get arrows working immediately.
 */

interface ArrowPositioningInput {
	arrow_type: 'blue' | 'red';
	motion_type: string;
	location: string;
	grid_mode: string;
	turns: number;
	letter?: string;
	start_orientation: string;
	end_orientation: string;
}

interface Position {
	x: number;
	y: number;
}

class SimpleArrowPositioning {
	async calculatePosition(input: ArrowPositioningInput): Promise<Position> {
		// Basic grid position mapping for common locations
		const gridPositions: Record<string, Position> = {
			n: { x: 475, y: 200 },
			s: { x: 475, y: 750 },
			e: { x: 750, y: 475 },
			w: { x: 200, y: 475 },
			ne: { x: 650, y: 300 },
			nw: { x: 300, y: 300 },
			se: { x: 650, y: 650 },
			sw: { x: 300, y: 650 },
		};

		// Get base position from location
		const basePosition = gridPositions[input.location.toLowerCase()] || { x: 475, y: 475 };

		// Create a copy to modify
		const position = { ...basePosition };

		// Add some variation based on motion type
		if (input.motion_type === 'pro') {
			position.x += 20;
		} else if (input.motion_type === 'anti') {
			position.x -= 20;
		}

		// Add small offset for blue vs red arrows
		if (input.arrow_type === 'blue') {
			position.y += 10;
		} else {
			position.y -= 10;
		}

		return position;
	}
}

// Export a singleton instance
export const simpleArrowPositioning = new SimpleArrowPositioning();
