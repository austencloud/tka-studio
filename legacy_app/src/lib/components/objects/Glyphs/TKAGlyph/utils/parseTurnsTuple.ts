// src/lib/components/objects/Glyphs/TKAGlyph/utils/parseTurnsTuple.ts
import type { DirRelation, PropRotDir, TKATurns } from '$lib/types/Types';

export const SAME = 's';
export const OPP = 'o';
export const CW = 'cw';
export const CCW = 'ccw';

const VALID_TURN_NUMS = [0, 0.5, 1, 1.5, 2, 2.5, 3] as const;
type ValidTurnNum = typeof VALID_TURN_NUMS[number];

export function parseTurnsTupleString(
  turnsStr: string
): [DirRelation | PropRotDir | null, TKATurns, TKATurns] {
  if (!turnsStr) return [null, 0, 0];

  const cleaned = turnsStr.replace(/[()]/g, '').trim();
  const parts = cleaned.split(',').map((p) => p.trim());

  // Destructure with proper defaults
  const [dirRaw = null, topRaw = null, bottomRaw = null] = parts;

  return [
    parseDirection(dirRaw),
    parseTurnValue(topRaw) ?? 0,
    parseTurnValue(bottomRaw) ?? 0
  ];
}

function parseDirection(item: string | null): DirRelation | PropRotDir | null {
  if (!item) return null;

  const validDirections = ['s', 'o', 'cw', 'ccw'] as const;
  return validDirections.includes(item as any)
    ? (item as DirRelation | PropRotDir)
    : null;
}

function parseTurnValue(item: string | null): TKATurns | null {
  if (!item) return null;
  if (item === 'fl') return 'fl';

  const num = Number(item);
  return !isNaN(num) && VALID_TURN_NUMS.includes(num as ValidTurnNum)
    ? (num as TKATurns)
    : null;
}
