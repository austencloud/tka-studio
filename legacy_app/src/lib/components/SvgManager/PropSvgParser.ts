// svgUtils.ts (new shared utilities)

import type { PropSvgData } from './PropSvgData';
import type { ArrowSvgData } from './ArrowSvgData';

type SvgData = PropSvgData | ArrowSvgData;

export const parsePropSvg = (svgText: string, propColor?: string): Omit<SvgData, 'imageSrc'> => {
	const doc = new DOMParser().parseFromString(svgText, 'image/svg+xml');
	const svg = doc.documentElement;

	// Add fallback viewBox
	const viewBoxValues = svg.getAttribute('viewBox')?.split(/\s+/) || ['0', '0', '100', '100'];
	const viewBox = {
		width: parseFloat(viewBoxValues[2]) || 100,
		height: parseFloat(viewBoxValues[3]) || 100
	};

	// Calculate safe center
	let center = { x: viewBox.width / 2, y: viewBox.height / 2 };

	try {
		const centerElement = doc.getElementById('centerPoint');
		if (centerElement) {
			center = {
				x: parseFloat(centerElement.getAttribute('cx') || '0') || center.x,
				y: parseFloat(centerElement.getAttribute('cy') || '0') || center.y
			};

		} else {
			console.warn(
				`⚠️ No centerPoint element found in SVG for ${propColor || 'unknown'} prop, using default center: (${center.x}, ${center.y})`
			);

			// Fallback for empty SVGs
			const firstPath = doc.querySelector('path');
			if (firstPath) {
				const bbox = firstPath.getBBox();
				center = {
					x: bbox.x + bbox.width / 2,
					y: bbox.y + bbox.height / 2
				};
			}
		}
	} catch (e) {
		console.warn('SVG center calculation failed, using default center');
	}

	return { viewBox, center };
};
