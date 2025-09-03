// src/lib/components/PlacementManagers/PropPlacementManager/DefaultPropPositioner.ts
import type { GridData } from '$lib/components/objects/Grid/GridData';
import type { GridPoint } from '$lib/components/objects/Grid/GridPoint';
import type { PropData } from '$lib/components/objects/Prop/PropData';

export class DefaultPropPositioner {
	private debugMode: boolean = true;
	private fallbackCoordinates: Record<string, { x: number; y: number }> = {
		// Default positions if grid points aren't found
		n: { x: 475, y: 330 },
		e: { x: 620, y: 475 },
		s: { x: 475, y: 620 },
		w: { x: 330, y: 475 },
		ne: { x: 620, y: 330 },
		se: { x: 620, y: 620 },
		sw: { x: 330, y: 620 },
		nw: { x: 330, y: 330 }
	};

	constructor(
		private gridData: GridData,
		private gridMode: string
	) {
		// Validate grid data on initialization
		if (!gridData || !gridData.allHandPointsNormal) {
			throw new Error('Invalid grid data provided to DefaultPropPositioner');
		}

		if (this.debugMode) {
			// Log some sample grid points to verify content
			const pointKeys = Object.keys(gridData.allHandPointsNormal).slice(0, 3);
		}
	}

	public async setToDefaultPosition(propData: PropData): Promise<void> {
		// Basic validation
		if (!propData || !propData.loc) {
			return;
		}

		this.updateCoords(propData);
	}

	public updateCoords(prop: PropData): void {

		const pointName = `${prop.loc}_${this.gridMode}_hand_point`;
		const gridPoint = this.getGridPoint(pointName);

		if (gridPoint && gridPoint.coordinates) {
			prop.coords = gridPoint.coordinates;

		} else {
			const fallback = this.getFallbackCoordinates(prop.loc);
			console.warn(
				`⚠️ Grid point "${pointName}" not found, using fallback: (${fallback.x}, ${fallback.y})`
			);
			prop.coords = fallback;

		}
	}

	private getGridPoint(pointName: string): GridPoint | null {
		// Try normal points first, then strict
		if (!this.gridData) {
			console.error('❌ Grid data is null when looking for point:', pointName);
			return null;
		}

		if (!this.gridData.allHandPointsNormal) {
			console.error('❌ allHandPointsNormal is null in grid data');
			return null;
		}

		const normalPoint = this.gridData.allHandPointsNormal[pointName];

		if (!normalPoint) {
			console.warn(`⚠️ Could not find normal point: "${pointName}"`);
		}

		const strictPoint = this.gridData.allHandPointsStrict
			? this.gridData.allHandPointsStrict[pointName]
			: null;

		return normalPoint || strictPoint;
	}

	private getFallbackCoordinates(loc: string): { x: number; y: number } {
		if (this.fallbackCoordinates[loc]) {
			return this.fallbackCoordinates[loc];
		}

		// If even the fallback isn't available, use center of grid
		if (this.gridData && this.gridData.centerPoint && this.gridData.centerPoint.coordinates) {
			return this.gridData.centerPoint.coordinates;
		}

		// Absolute last resort
		return { x: 475, y: 475 };
	}
}
