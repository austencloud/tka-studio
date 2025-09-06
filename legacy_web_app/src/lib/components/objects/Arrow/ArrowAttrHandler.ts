export default class ArrowAttrHandler {
	color: string;
	motion: {
		startLoc: string;
		endLoc: string;
		type: string;
		propRotDir?: string;
	};
	arrowProps: any;

	constructor(arrowProps: any) {
		this.arrowProps = arrowProps;
		this.color = arrowProps.color;
		this.motion = arrowProps.motion;
	}

	updateAttributes(newAttributes: Partial<typeof this.arrowProps>) {
		Object.assign(this.arrowProps, newAttributes);
		this.color = this.arrowProps.color;
		this.motion = this.arrowProps.motion;
	}
}
