export type Position =
  | 'alpha1_alpha1'
  | 'alpha2_alpha2'
  | 'beta4_beta4'
  | 'beta5_beta5'
  | 'gamma11_gamma11'
  | 'gamma12_gamma12';

export type GridMode = 'diamond' | 'other';

class PositionMapper {
  private readonly POSITION_MAPPING: Record<GridMode, Position[]> = {
    diamond: ['alpha1_alpha1', 'beta5_beta5', 'gamma11_gamma11'],
    other: ['alpha2_alpha2', 'beta4_beta4', 'gamma12_gamma12']
  };

  private readonly VERTICAL_MIRROR_MAP: Record<Position, Position> = {
    'alpha1_alpha1': 'alpha2_alpha2',
    'alpha2_alpha2': 'alpha1_alpha1',
    'beta4_beta4': 'beta5_beta5',
    'beta5_beta5': 'beta4_beta4',
    'gamma11_gamma11': 'gamma12_gamma12',
    'gamma12_gamma12': 'gamma11_gamma11'
  };

  private readonly ROTATION_MAP: Record<Position, Position> = {
    'alpha1_alpha1': 'beta5_beta5',
    'beta5_beta5': 'gamma11_gamma11',
    'gamma11_gamma11': 'alpha2_alpha2',
    'alpha2_alpha2': 'beta4_beta4',
    'beta4_beta4': 'gamma12_gamma12',
    'gamma12_gamma12': 'alpha1_alpha1'
  };

  mapPosition(
    beatIndex: number,
    gridMode: GridMode = 'diamond'
  ): Position {
    const positions = this.POSITION_MAPPING[gridMode];
    return positions[beatIndex % positions.length];
  }

  mirrorPosition(position: Position): Position {
    return this.VERTICAL_MIRROR_MAP[position] || position;
  }

  rotatePosition(position: Position): Position {
    return this.ROTATION_MAP[position] || position;
  }

  // Advanced: Find possible positions between two locations
  findPositionPath(
    startPos: Position,
    endPos: Position
  ): Position[] {
    // This would implement logic to find valid transitions between positions
    // Placeholder for now
    return [startPos, endPos];
  }
}

export const positionUtils = new PositionMapper();
