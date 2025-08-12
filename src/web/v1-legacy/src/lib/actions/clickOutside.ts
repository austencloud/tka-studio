// src/lib/actions/clickOutside.ts
type ClickOutsideAction = (
	node: HTMLElement,
	callback: () => void
) => {
	destroy: () => void;
};

export const clickOutside: ClickOutsideAction = (node, callback) => {
	const handleClick = (event: MouseEvent) => {
		if (node && !node.contains(event.target as Node) && !event.defaultPrevented) {
			callback();
		}
	};

	document.addEventListener('click', handleClick, true);

	return {
		destroy() {
			document.removeEventListener('click', handleClick, true);
		}
	};
};
