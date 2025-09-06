// Define base setting type
export type BaseSetting = {
	label: string;
};

// Define all specific setting types
export type ToggleSetting = BaseSetting & {
	type: 'toggle';
	defaultValue: boolean;
};

export type NumberSetting = BaseSetting & {
	type: 'number';
	defaultValue: number;
	min: number;
	max: number;
};

export type RangeSetting = BaseSetting & {
	type: 'range';
	defaultValue: number;
	min: number;
	max: number;
};

export type SelectSetting = BaseSetting & {
	type: 'select';
	defaultValue: string;
	options: string[];
};

export type TextSetting = BaseSetting & {
	type: 'text';
	defaultValue: string;
};

export type ColorSetting = BaseSetting & {
	type: 'color';
	defaultValue: string;
};

export type CustomSetting = BaseSetting & {
	type: 'custom';
	component: string;
	defaultValue?: any; // Optional default value for custom components
};

// Union type of all settings
export type Setting =
	| ToggleSetting
	| NumberSetting
	| RangeSetting
	| SelectSetting
	| TextSetting
	| ColorSetting
	| CustomSetting;