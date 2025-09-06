/**
 * Type definitions for the Workbench Button Panel
 */

// Layout orientation types
export type LayoutOrientation = 'vertical' | 'horizontal';

// Button definition interface
export interface ButtonDefinition {
	icon: string; // Font Awesome icon class (e.g., 'fa-save')
	title: string; // Button tooltip/aria-label
	id: string; // Unique identifier for the button action
	color?: string; // Optional: Specific color for the button border/hover
	disabled?: boolean; // Optional: Whether the button is disabled
}

// Panel state interface managed by the store
export interface PanelState {
	layout: LayoutOrientation; // Current layout mode
}

// Props expected by the main ButtonPanel component
export interface ButtonPanelProps {
	containerWidth: number; // Width of the parent container
	containerHeight: number; // Height of the parent container
	isPortrait: boolean; // Orientation flag
	buttons: ButtonDefinition[]; // Array of button definitions
}

// Type for the event dispatched when an action button is clicked
export interface ActionEventDetail {
	id: string; // The ID of the button that was clicked
}
