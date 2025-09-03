import type { HandRotDir } from '$lib/types/Types';

export class HandpathCalculator {
	private handRotDirMap: Record<string, string>;

	constructor() {
		const clockwisePairs = [
			['s', 'w'],
			['w', 'n'],
			['n', 'e'],
			['e', 's']
		];
		const counterClockwisePairs = [
			['w', 's'],
			['n', 'w'],
			['e', 'n'],
			['s', 'e']
		];
		const diagonalClockwise = [
			['ne', 'se'],
			['se', 'sw'],
			['sw', 'nw'],
			['nw', 'ne']
		];
		const diagonalCounterClockwise = [
			['ne', 'nw'],
			['nw', 'sw'],
			['sw', 'se'],
			['se', 'ne']
		];
		const dashPairs = [
			['s', 'n'],
			['w', 'e'],
			['n', 's'],
			['e', 'w'],
			['ne', 'sw'],
			['se', 'nw'],
			['sw', 'ne'],
			['nw', 'se']
		];
		const staticPairs = [
			['n', 'n'],
			['e', 'e'],
			['s', 's'],
			['w', 'w'],
			['ne', 'ne'],
			['se', 'se'],
			['sw', 'sw'],
			['nw', 'nw']
		];

		this.handRotDirMap = {
			...Object.fromEntries(clockwisePairs.map((pair) => [pair.join(','), 'cw_shift'])),
			...Object.fromEntries(counterClockwisePairs.map((pair) => [pair.join(','), 'ccw_shift'])),
			...Object.fromEntries(diagonalClockwise.map((pair) => [pair.join(','), 'cw_shift'])),
			...Object.fromEntries(diagonalCounterClockwise.map((pair) => [pair.join(','), 'ccw_shift'])),
			...Object.fromEntries(dashPairs.map((pair) => [pair.join(','), 'dash'])),
			...Object.fromEntries(staticPairs.map((pair) => [pair.join(','), 'static']))
		};
	}

	getHandRotDir(startLoc: string, endLoc: string): HandRotDir {
		return (this.handRotDirMap[`${startLoc},${endLoc}`] as HandRotDir) || null;
	}
}
