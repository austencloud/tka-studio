/**
 * GridPositionDeriver Tests
 *
 * HIGH VALUE TESTS (9/10) - Critical domain logic that prevents:
 * - Wrong positions shown in pictographs
 * - Incorrect hand location mappings
 * - Invalid position derivations
 *
 * This service maps between grid positions (alpha1, beta2, etc.) and hand location pairs.
 * Wrong mappings = wrong movements shown to users = catastrophic UX failure.
 */

import { beforeEach, describe, expect, it } from "vitest";
import {
  GridLocation,
  GridPosition,
} from "../../../src/lib/shared/pictograph/grid/domain/enums/grid-enums";
import { GridPositionDeriver } from "../../../src/lib/shared/pictograph/grid/services/implementations/GridPositionDeriver";

describe("GridPositionDeriver", () => {
  let service: GridPositionDeriver;

  beforeEach(() => {
    service = new GridPositionDeriver();
  });

  // ============================================================================
  // ALPHA POSITIONS - Opposite/Complementary Directions (8 positions)
  // ============================================================================

  describe("Alpha Positions - Bidirectional Mapping", () => {
    it("should map ALPHA1: SOUTH,NORTH ↔ alpha1", () => {
      // Position → Locations
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA1
      );
      expect(blue).toBe(GridLocation.SOUTH);
      expect(red).toBe(GridLocation.NORTH);

      // Locations → Position
      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTH,
        GridLocation.NORTH
      );
      expect(position).toBe(GridPosition.ALPHA1);
    });

    it("should map ALPHA2: SOUTHWEST,NORTHEAST ↔ alpha2", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA2
      );
      expect(blue).toBe(GridLocation.SOUTHWEST);
      expect(red).toBe(GridLocation.NORTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHWEST,
        GridLocation.NORTHEAST
      );
      expect(position).toBe(GridPosition.ALPHA2);
    });

    it("should map ALPHA3: WEST,EAST ↔ alpha3", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA3
      );
      expect(blue).toBe(GridLocation.WEST);
      expect(red).toBe(GridLocation.EAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.WEST,
        GridLocation.EAST
      );
      expect(position).toBe(GridPosition.ALPHA3);
    });

    it("should map ALPHA4: NORTHWEST,SOUTHEAST ↔ alpha4", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA4
      );
      expect(blue).toBe(GridLocation.NORTHWEST);
      expect(red).toBe(GridLocation.SOUTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHWEST,
        GridLocation.SOUTHEAST
      );
      expect(position).toBe(GridPosition.ALPHA4);
    });

    it("should map ALPHA5: NORTH,SOUTH ↔ alpha5", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA5
      );
      expect(blue).toBe(GridLocation.NORTH);
      expect(red).toBe(GridLocation.SOUTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTH,
        GridLocation.SOUTH
      );
      expect(position).toBe(GridPosition.ALPHA5);
    });

    it("should map ALPHA6: NORTHEAST,SOUTHWEST ↔ alpha6", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA6
      );
      expect(blue).toBe(GridLocation.NORTHEAST);
      expect(red).toBe(GridLocation.SOUTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHEAST,
        GridLocation.SOUTHWEST
      );
      expect(position).toBe(GridPosition.ALPHA6);
    });

    it("should map ALPHA7: EAST,WEST ↔ alpha7", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA7
      );
      expect(blue).toBe(GridLocation.EAST);
      expect(red).toBe(GridLocation.WEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.EAST,
        GridLocation.WEST
      );
      expect(position).toBe(GridPosition.ALPHA7);
    });

    it("should map ALPHA8: SOUTHEAST,NORTHWEST ↔ alpha8", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.ALPHA8
      );
      expect(blue).toBe(GridLocation.SOUTHEAST);
      expect(red).toBe(GridLocation.NORTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHEAST,
        GridLocation.NORTHWEST
      );
      expect(position).toBe(GridPosition.ALPHA8);
    });
  });

  // ============================================================================
  // BETA POSITIONS - Same Direction (8 positions)
  // ============================================================================

  describe("Beta Positions - Bidirectional Mapping", () => {
    it("should map BETA1: NORTH,NORTH ↔ beta1", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA1
      );
      expect(blue).toBe(GridLocation.NORTH);
      expect(red).toBe(GridLocation.NORTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTH,
        GridLocation.NORTH
      );
      expect(position).toBe(GridPosition.BETA1);
    });

    it("should map BETA2: NORTHEAST,NORTHEAST ↔ beta2", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA2
      );
      expect(blue).toBe(GridLocation.NORTHEAST);
      expect(red).toBe(GridLocation.NORTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHEAST,
        GridLocation.NORTHEAST
      );
      expect(position).toBe(GridPosition.BETA2);
    });

    it("should map BETA3: EAST,EAST ↔ beta3", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA3
      );
      expect(blue).toBe(GridLocation.EAST);
      expect(red).toBe(GridLocation.EAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.EAST,
        GridLocation.EAST
      );
      expect(position).toBe(GridPosition.BETA3);
    });

    it("should map BETA4: SOUTHEAST,SOUTHEAST ↔ beta4", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA4
      );
      expect(blue).toBe(GridLocation.SOUTHEAST);
      expect(red).toBe(GridLocation.SOUTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHEAST,
        GridLocation.SOUTHEAST
      );
      expect(position).toBe(GridPosition.BETA4);
    });

    it("should map BETA5: SOUTH,SOUTH ↔ beta5", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA5
      );
      expect(blue).toBe(GridLocation.SOUTH);
      expect(red).toBe(GridLocation.SOUTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTH,
        GridLocation.SOUTH
      );
      expect(position).toBe(GridPosition.BETA5);
    });

    it("should map BETA6: SOUTHWEST,SOUTHWEST ↔ beta6", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA6
      );
      expect(blue).toBe(GridLocation.SOUTHWEST);
      expect(red).toBe(GridLocation.SOUTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHWEST,
        GridLocation.SOUTHWEST
      );
      expect(position).toBe(GridPosition.BETA6);
    });

    it("should map BETA7: WEST,WEST ↔ beta7", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA7
      );
      expect(blue).toBe(GridLocation.WEST);
      expect(red).toBe(GridLocation.WEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.WEST,
        GridLocation.WEST
      );
      expect(position).toBe(GridPosition.BETA7);
    });

    it("should map BETA8: NORTHWEST,NORTHWEST ↔ beta8", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.BETA8
      );
      expect(blue).toBe(GridLocation.NORTHWEST);
      expect(red).toBe(GridLocation.NORTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHWEST,
        GridLocation.NORTHWEST
      );
      expect(position).toBe(GridPosition.BETA8);
    });
  });

  // ============================================================================
  // GAMMA POSITIONS - Mixed/Varied Combinations (16 positions)
  // ============================================================================

  describe("Gamma Positions (1-8) - Bidirectional Mapping", () => {
    it("should map GAMMA1: WEST,NORTH ↔ gamma1", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA1
      );
      expect(blue).toBe(GridLocation.WEST);
      expect(red).toBe(GridLocation.NORTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.WEST,
        GridLocation.NORTH
      );
      expect(position).toBe(GridPosition.GAMMA1);
    });

    it("should map GAMMA2: NORTHWEST,NORTHEAST ↔ gamma2", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA2
      );
      expect(blue).toBe(GridLocation.NORTHWEST);
      expect(red).toBe(GridLocation.NORTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHWEST,
        GridLocation.NORTHEAST
      );
      expect(position).toBe(GridPosition.GAMMA2);
    });

    it("should map GAMMA3: NORTH,EAST ↔ gamma3", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA3
      );
      expect(blue).toBe(GridLocation.NORTH);
      expect(red).toBe(GridLocation.EAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTH,
        GridLocation.EAST
      );
      expect(position).toBe(GridPosition.GAMMA3);
    });

    it("should map GAMMA4: NORTHEAST,SOUTHEAST ↔ gamma4", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA4
      );
      expect(blue).toBe(GridLocation.NORTHEAST);
      expect(red).toBe(GridLocation.SOUTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHEAST,
        GridLocation.SOUTHEAST
      );
      expect(position).toBe(GridPosition.GAMMA4);
    });

    it("should map GAMMA5: EAST,SOUTH ↔ gamma5", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA5
      );
      expect(blue).toBe(GridLocation.EAST);
      expect(red).toBe(GridLocation.SOUTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.EAST,
        GridLocation.SOUTH
      );
      expect(position).toBe(GridPosition.GAMMA5);
    });

    it("should map GAMMA6: SOUTHEAST,SOUTHWEST ↔ gamma6", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA6
      );
      expect(blue).toBe(GridLocation.SOUTHEAST);
      expect(red).toBe(GridLocation.SOUTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHEAST,
        GridLocation.SOUTHWEST
      );
      expect(position).toBe(GridPosition.GAMMA6);
    });

    it("should map GAMMA7: SOUTH,WEST ↔ gamma7", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA7
      );
      expect(blue).toBe(GridLocation.SOUTH);
      expect(red).toBe(GridLocation.WEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTH,
        GridLocation.WEST
      );
      expect(position).toBe(GridPosition.GAMMA7);
    });

    it("should map GAMMA8: SOUTHWEST,NORTHWEST ↔ gamma8", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA8
      );
      expect(blue).toBe(GridLocation.SOUTHWEST);
      expect(red).toBe(GridLocation.NORTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHWEST,
        GridLocation.NORTHWEST
      );
      expect(position).toBe(GridPosition.GAMMA8);
    });
  });

  describe("Gamma Positions (9-16) - Bidirectional Mapping", () => {
    it("should map GAMMA9: EAST,NORTH ↔ gamma9", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA9
      );
      expect(blue).toBe(GridLocation.EAST);
      expect(red).toBe(GridLocation.NORTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.EAST,
        GridLocation.NORTH
      );
      expect(position).toBe(GridPosition.GAMMA9);
    });

    it("should map GAMMA10: SOUTHEAST,NORTHEAST ↔ gamma10", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA10
      );
      expect(blue).toBe(GridLocation.SOUTHEAST);
      expect(red).toBe(GridLocation.NORTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHEAST,
        GridLocation.NORTHEAST
      );
      expect(position).toBe(GridPosition.GAMMA10);
    });

    it("should map GAMMA11: SOUTH,EAST ↔ gamma11", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA11
      );
      expect(blue).toBe(GridLocation.SOUTH);
      expect(red).toBe(GridLocation.EAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTH,
        GridLocation.EAST
      );
      expect(position).toBe(GridPosition.GAMMA11);
    });

    it("should map GAMMA12: SOUTHWEST,SOUTHEAST ↔ gamma12", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA12
      );
      expect(blue).toBe(GridLocation.SOUTHWEST);
      expect(red).toBe(GridLocation.SOUTHEAST);

      const position = service.getGridPositionFromLocations(
        GridLocation.SOUTHWEST,
        GridLocation.SOUTHEAST
      );
      expect(position).toBe(GridPosition.GAMMA12);
    });

    it("should map GAMMA13: WEST,SOUTH ↔ gamma13", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA13
      );
      expect(blue).toBe(GridLocation.WEST);
      expect(red).toBe(GridLocation.SOUTH);

      const position = service.getGridPositionFromLocations(
        GridLocation.WEST,
        GridLocation.SOUTH
      );
      expect(position).toBe(GridPosition.GAMMA13);
    });

    it("should map GAMMA14: NORTHWEST,SOUTHWEST ↔ gamma14", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA14
      );
      expect(blue).toBe(GridLocation.NORTHWEST);
      expect(red).toBe(GridLocation.SOUTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHWEST,
        GridLocation.SOUTHWEST
      );
      expect(position).toBe(GridPosition.GAMMA14);
    });

    it("should map GAMMA15: NORTH,WEST ↔ gamma15", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA15
      );
      expect(blue).toBe(GridLocation.NORTH);
      expect(red).toBe(GridLocation.WEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTH,
        GridLocation.WEST
      );
      expect(position).toBe(GridPosition.GAMMA15);
    });

    it("should map GAMMA16: NORTHEAST,NORTHWEST ↔ gamma16", () => {
      const [blue, red] = service.getGridLocationsFromPosition(
        GridPosition.GAMMA16
      );
      expect(blue).toBe(GridLocation.NORTHEAST);
      expect(red).toBe(GridLocation.NORTHWEST);

      const position = service.getGridPositionFromLocations(
        GridLocation.NORTHEAST,
        GridLocation.NORTHWEST
      );
      expect(position).toBe(GridPosition.GAMMA16);
    });
  });

  // ============================================================================
  // ERROR HANDLING - Invalid Inputs
  // ============================================================================

  describe("Error Handling", () => {
    it("should throw error for invalid position in getGridLocationsFromPosition", () => {
      const invalidPosition = "invalid_position" as GridPosition;

      expect(() =>
        service.getGridLocationsFromPosition(invalidPosition)
      ).toThrow("No location pair found for position: invalid_position");
    });

    it("should throw error for unmapped location pair in getGridPositionFromLocations", () => {
      // This combination doesn't exist in the mapping
      // (NORTH, NORTHEAST is not a valid position)
      expect(() =>
        service.getGridPositionFromLocations(
          GridLocation.NORTH,
          GridLocation.NORTHEAST
        )
      ).toThrow("No position found for locations: n, ne");
    });

    it("should throw error for another unmapped location pair", () => {
      // (SOUTH, NORTHEAST is not a valid position)
      expect(() =>
        service.getGridPositionFromLocations(
          GridLocation.SOUTH,
          GridLocation.NORTHEAST
        )
      ).toThrow("No position found for locations: s, ne");
    });
  });

  // ============================================================================
  // COMPREHENSIVE COVERAGE - All 32 Positions
  // ============================================================================

  describe("Complete Position Coverage", () => {
    it("should have exactly 32 total positions mapped", () => {
      const allPositions = [
        // Alpha (8)
        GridPosition.ALPHA1,
        GridPosition.ALPHA2,
        GridPosition.ALPHA3,
        GridPosition.ALPHA4,
        GridPosition.ALPHA5,
        GridPosition.ALPHA6,
        GridPosition.ALPHA7,
        GridPosition.ALPHA8,
        // Beta (8)
        GridPosition.BETA1,
        GridPosition.BETA2,
        GridPosition.BETA3,
        GridPosition.BETA4,
        GridPosition.BETA5,
        GridPosition.BETA6,
        GridPosition.BETA7,
        GridPosition.BETA8,
        // Gamma (16)
        GridPosition.GAMMA1,
        GridPosition.GAMMA2,
        GridPosition.GAMMA3,
        GridPosition.GAMMA4,
        GridPosition.GAMMA5,
        GridPosition.GAMMA6,
        GridPosition.GAMMA7,
        GridPosition.GAMMA8,
        GridPosition.GAMMA9,
        GridPosition.GAMMA10,
        GridPosition.GAMMA11,
        GridPosition.GAMMA12,
        GridPosition.GAMMA13,
        GridPosition.GAMMA14,
        GridPosition.GAMMA15,
        GridPosition.GAMMA16,
      ];

      // Verify all positions can be converted to locations and back
      allPositions.forEach((position) => {
        const [blue, red] = service.getGridLocationsFromPosition(position);
        const derivedPosition = service.getGridPositionFromLocations(blue, red);
        expect(derivedPosition).toBe(position);
      });

      expect(allPositions.length).toBe(32);
    });

    it("should maintain bidirectional consistency for all positions", () => {
      // Test that every position → locations → position round-trip works
      const positions = Object.values(GridPosition);

      positions.forEach((position) => {
        const [blue, red] = service.getGridLocationsFromPosition(position);
        const roundTrip = service.getGridPositionFromLocations(blue, red);
        expect(roundTrip).toBe(position);
      });
    });
  });
});
