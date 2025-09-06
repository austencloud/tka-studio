import type { ArrowSvgData } from './ArrowSvgData';

// ArrowSvgParser.ts
export const parseArrowSvg = (svgText: string): ArrowSvgData => {
	const viewBoxMatch = svgText.match(/viewBox="([^"]+)"/);
	const viewBoxParts = viewBoxMatch ? viewBoxMatch[1].split(' ').map(Number) : [0, 0, 100, 100];
	return {
		imageSrc: '', // Add a default or appropriate value for imageSrc
		viewBox: {
			x: viewBoxParts[0],
			y: viewBoxParts[1],
			width: viewBoxParts[2],
			height: viewBoxParts[3]
		},
		center: { x: viewBoxParts[2] / 2, y: viewBoxParts[3] / 2 }
	};
}

