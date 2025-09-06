// PropClassifier.ts

import type { PropData } from '../PropData';
import { PropType } from './PropTypes';

const smallUnilateral = [PropType.CLUB];
const smallBilateral = [PropType.TRIAD, PropType.MINIHOOP];

export class PropClassifier {
	smallUni: any;
	smallBi: any;
	hands: any;
	bigProps: any[];
	smallProps: any[];
	bigUni: any;
	bigBi: any;

	constructor(props: PropData[]) {
		props.forEach((prop) => {
			if (smallUnilateral.includes(prop.propType)) {
				this.smallUni.push(prop);
			} else if (smallBilateral.includes(prop.propType)) {
				this.smallBi.push(prop);
			} else if (prop.propType === PropType.HAND) {
				this.hands.push(prop);
			}
		});

		this.bigProps = [...this.bigUni, ...this.bigBi];
		this.smallProps = [...this.smallUni, ...this.smallBi];
	}
}
