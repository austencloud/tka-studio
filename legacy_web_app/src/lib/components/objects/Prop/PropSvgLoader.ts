// PropSvgLoader.ts

import type { PropSvgData } from "$lib/components/SvgManager/PropSvgData";

const parseViewBox = (svg: SVGElement) => {
	const [, , w, h] = svg.getAttribute('viewBox')?.split(/\s+/) || [];
	return { width: parseFloat(w), height: parseFloat(h) };
};

const getCenterPoint = (doc: Document, viewBox: PropSvgData['viewBox']) => {
	const element = doc.getElementById('centerPoint');
	if (!element)
		return {
			x: viewBox.width / 2,
			y: viewBox.height / 2
		};

	return {
		x: parseFloat(element.getAttribute('cx') || '0'),
		y: parseFloat(element.getAttribute('cy') || '0')
	};
};

export default class PropSvgLoader {
	static async load(propType: string): Promise<PropSvgData> {
		const response = await fetch(`/images/props/${propType}.svg`);
		if (!response.ok) throw new Error(`Failed to load prop SVG: ${propType}`);

		const svgText = await response.text();
		const doc = new DOMParser().parseFromString(svgText, 'image/svg+xml');
		const svg = doc.documentElement;

		const viewBox = parseViewBox(svg as unknown as SVGElement);
		const center = getCenterPoint(doc, viewBox);

		return {
			imageSrc: `data:image/svg+xml;base64,${btoa(svgText)}`,
			viewBox,
			center
		};
	}
}
