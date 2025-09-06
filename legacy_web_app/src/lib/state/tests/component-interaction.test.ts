/**
 * Component Interaction Tests
 *
 * Tests how UI components interact with the state management system.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { get, writable } from 'svelte/store';
import { stateRegistry } from '../core/registry';
import { createStore } from '../core/store';
import { resetAllState } from '../core/testing';
import { createMachine, assign, type AnyActorRef } from 'xstate';

// Mock counter store
const createMockCounterStore = () => {
	interface CounterState {
		value: number;
	}

	const store = writable<CounterState>({ value: 0 });
	const counterStore = {
		subscribe: store.subscribe,
		increment: () => {
			store.update((state: CounterState) => ({ value: state.value + 1 }));
		},
		decrement: () => {
			store.update((state: CounterState) => ({ value: state.value - 1 }));
		},
		setValue: (value: number) => {
			store.set({ value });
		}
	};

	return {
		counterStore,
		reset: () => {
			store.set({ value: 0 });
		}
	};
};

describe('Component Interaction with State', () => {
	let mockStore: ReturnType<typeof createMockCounterStore>;

	beforeEach(() => {
		vi.resetAllMocks();
		resetAllState();
		mockStore = createMockCounterStore();
	});

	afterEach(() => {
		vi.restoreAllMocks();
	});

	describe('UI Events Updating State', () => {
		it('updates store when component event is triggered', async () => {
			// Create a store that will be updated by component events
			interface CountStore {
				count: number;
			}

			const store = createStore<CountStore, { increment: () => void; decrement: () => void }>(
				'uiStore',
				{ count: 0 },
				(set) => ({
					increment: () => set({ count: get(store).count + 1 }),
					decrement: () => set({ count: get(store).count - 1 })
				})
			);

			// Simulate a component event handler triggering store updates
			const triggerIncrement = () => store.increment();
			const triggerDecrement = () => store.decrement();

			// Initial state
			expect(get(store).count).toBe(0);

			// Simulate a user clicking the increment button
			triggerIncrement();

			// Verify store was updated
			expect(get(store).count).toBe(1);

			// Simulate a user clicking the decrement button
			triggerDecrement();

			// Verify store was updated again
			expect(get(store).count).toBe(0);
		});

		it('handles multiple UI interactions in sequence', async () => {
			// Define the tab store types
			interface TabData {
				name: string;
				items: string[];
			}

			interface TabsState {
				activeTab: number;
				tabData: TabData[];
			}

			// A store with more complex state
			const uiStateStore = createStore<
				TabsState,
				{
					setActiveTab: (tabIndex: number) => void;
					addItem: (tabIndex: number, item: string) => void;
				}
			>(
				'uiStateStore',
				{
					activeTab: 0,
					tabData: [
						{ name: 'Tab 1', items: [] },
						{ name: 'Tab 2', items: [] },
						{ name: 'Tab 3', items: [] }
					]
				},
				(set) => ({
					setActiveTab: (tabIndex: number) => set({ ...get(uiStateStore), activeTab: tabIndex }),
					addItem: (tabIndex: number, item: string) => {
						const currentState = get(uiStateStore);
						const newTabData = [...currentState.tabData];
						newTabData[tabIndex] = {
							...newTabData[tabIndex],
							items: [...newTabData[tabIndex].items, item]
						};
						return set({ ...currentState, tabData: newTabData });
					}
				})
			);

			// Simulate UI interactions
			// Change active tab
			uiStateStore.setActiveTab(1);

			// Add items to the active tab
			uiStateStore.addItem(1, 'New Item 1');
			uiStateStore.addItem(1, 'New Item 2');

			// Change tab again
			uiStateStore.setActiveTab(2);

			// Add an item to the new active tab
			uiStateStore.addItem(2, 'Tab 3 Item');

			// Verify final state
			const state = get(uiStateStore);
			expect(state.activeTab).toBe(2);
			expect(state.tabData[1].items).toEqual(['New Item 1', 'New Item 2']);
			expect(state.tabData[2].items).toEqual(['Tab 3 Item']);
		});

		it('updates store directly using store actions', async () => {
			const { counterStore } = mockStore;

			// Initial state
			expect(get(counterStore).value).toBe(0);

			// Simulate user interaction that triggers the store action
			counterStore.increment();

			// Verify store was updated
			expect(get(counterStore).value).toBe(1);
		});
	});

	describe('State Updates Triggering UI Changes', () => {
		it('demonstrates how UI would update when store changes', async () => {
			// We'll simulate a UI component with this render function
			const renderCount = (count: number): string => `Count: ${count}`;

			const { counterStore } = mockStore;

			// Initial store value
			counterStore.setValue(5);

			// Render UI based on store value (simulating what a component would do)
			let displayText = renderCount(get(counterStore).value);
			expect(displayText).toBe('Count: 5');

			// Update the store
			counterStore.setValue(10);

			// Re-render UI to simulate reactivity
			displayText = renderCount(get(counterStore).value);
			expect(displayText).toBe('Count: 10');
		});

		it('handles complex state to UI mapping', async () => {
			// Define form field types
			interface FormField {
				value: string;
				valid: boolean;
				error: string | null;
			}

			interface FormState {
				fields: {
					name: FormField;
					email: FormField;
					age: FormField;
				};
				formValid: boolean;
				submitting: boolean;
				submitted: boolean;
			}

			// Create a store with complex state
			const formStore = createStore<
				FormState,
				{
					updateField: (field: keyof FormState['fields'], value: string) => void;
					setSubmitting: (submitting: boolean) => void;
					setSubmitted: (submitted: boolean) => void;
				}
			>(
				'formStore',
				{
					fields: {
						name: { value: '', valid: true, error: null },
						email: { value: '', valid: true, error: null },
						age: { value: '', valid: true, error: null }
					},
					formValid: true,
					submitting: false,
					submitted: false
				},
				(set) => ({
					updateField: (field: keyof FormState['fields'], value: string) => {
						const currentState = get(formStore);

						// Validate the field
						let valid = true;
						let error = null;

						if (field === 'name' && (!value || value.length < 2)) {
							valid = false;
							error = 'Name must be at least 2 characters';
						} else if (field === 'email' && (!value || !value.includes('@'))) {
							valid = false;
							error = 'Email must be valid';
						} else if (field === 'age' && (!value || isNaN(Number(value)) || +value < 18)) {
							valid = false;
							error = 'Age must be at least 18';
						}

						// Update the field
						const newFields = {
							...currentState.fields,
							[field]: { value, valid, error }
						};

						// Check if form is valid
						const formValid = Object.values(newFields).every((field) => field.valid);

						return set({
							...currentState,
							fields: newFields,
							formValid
						});
					},
					setSubmitting: (submitting: boolean) => set({ ...get(formStore), submitting }),
					setSubmitted: (submitted: boolean) => set({ ...get(formStore), submitted })
				})
			);

			// Test updating form fields
			formStore.updateField('name', 'John');
			formStore.updateField('email', 'john@example.com');
			formStore.updateField('age', '25');

			// Check form state
			let state = get(formStore);
			expect(state.formValid).toBe(true);
			expect(state.fields.name.valid).toBe(true);
			expect(state.fields.email.valid).toBe(true);
			expect(state.fields.age.valid).toBe(true);

			// Test invalid input
			formStore.updateField('email', 'invalid-email');

			// Check form state
			state = get(formStore);
			expect(state.formValid).toBe(false);
			expect(state.fields.email.valid).toBe(false);
			expect(state.fields.email.error).toBe('Email must be valid');

			// Simulate form submission process
			formStore.updateField('email', 'john@example.com'); // Fix the email
			formStore.setSubmitting(true);

			// Check submitting state
			state = get(formStore);
			expect(state.formValid).toBe(true);
			expect(state.submitting).toBe(true);

			// Complete submission
			formStore.setSubmitting(false);
			formStore.setSubmitted(true);

			// Check final state
			state = get(formStore);
			expect(state.submitting).toBe(false);
			expect(state.submitted).toBe(true);
		});
	});

	describe('UI Component Integration with XState', () => {
		// Define the wizard machine types
		interface WizardContext {
			formData: {
				step1: Record<string, string>;
				step2: Record<string, string>;
				step3: Record<string, string>;
			};
		}

		interface UpdateEvent {
			type: 'UPDATE';
			field: string;
			value: string;
		}

		type WizardEvent = { type: 'NEXT' } | { type: 'PREV' } | { type: 'SUBMIT' } | UpdateEvent;

		// Create a simple state machine for wizard UI
		const wizardMachine = createMachine({
			id: 'wizard',
			initial: 'step1',
			context: {
				formData: {
					step1: {},
					step2: {},
					step3: {}
				}
			},
			types: {} as {
				context: WizardContext;
				events: WizardEvent;
			},
			states: {
				step1: {
					on: {
						NEXT: {
							target: 'step2'
						},
						UPDATE: {
							actions: assign({
								formData: ({ context, event }) => ({
									...context.formData,
									step1: {
										...context.formData.step1,
										[event.field]: event.value
									}
								})
							})
						}
					}
				},
				step2: {
					on: {
						PREV: {
							target: 'step1'
						},
						NEXT: {
							target: 'step3'
						},
						UPDATE: {
							actions: assign({
								formData: ({ context, event }) => ({
									...context.formData,
									step2: {
										...context.formData.step2,
										[event.field]: event.value
									}
								})
							})
						}
					}
				},
				step3: {
					on: {
						PREV: {
							target: 'step2'
						},
						SUBMIT: {
							target: 'complete'
						},
						UPDATE: {
							actions: assign({
								formData: ({ context, event }) => ({
									...context.formData,
									step3: {
										...context.formData.step3,
										[event.field]: event.value
									}
								})
							})
						}
					}
				},
				complete: {
					type: 'final'
				}
			}
		});

		it('synchronizes UI state with XState machine', async () => {
			// Create the actor from the machine
			const wizardActor = stateRegistry.registerMachine('wizardMachine', wizardMachine);

			// Check initial state
			expect(wizardActor.getSnapshot().value).toBe('step1');

			// Simulate user filling out step 1
			wizardActor.send({
				type: 'UPDATE',
				field: 'name',
				value: 'John Doe'
			});

			wizardActor.send({
				type: 'UPDATE',
				field: 'email',
				value: 'john@example.com'
			});

			// Check data was updated
			const contextAfterStep1 = wizardActor.getSnapshot().context as WizardContext;
			expect(contextAfterStep1.formData.step1).toEqual({
				name: 'John Doe',
				email: 'john@example.com'
			});

			// Move to next step
			wizardActor.send({ type: 'NEXT' });

			// Check state changed
			expect(wizardActor.getSnapshot().value).toBe('step2');

			// Fill out step 2
			wizardActor.send({
				type: 'UPDATE',
				field: 'address',
				value: '123 Main St'
			});

			// Move to step 3
			wizardActor.send({ type: 'NEXT' });
			expect(wizardActor.getSnapshot().value).toBe('step3');

			// Fill out step 3
			wizardActor.send({
				type: 'UPDATE',
				field: 'comments',
				value: 'Test comment'
			});

			// Submit form
			wizardActor.send({ type: 'SUBMIT' });

			// Check final state
			expect(wizardActor.getSnapshot().value).toBe('complete');

			// Verify all data was collected
			const formData = (wizardActor.getSnapshot().context as WizardContext).formData;
			expect(formData).toEqual({
				step1: { name: 'John Doe', email: 'john@example.com' },
				step2: { address: '123 Main St' },
				step3: { comments: 'Test comment' }
			});
		});

		it('handles navigation between wizard steps', async () => {
			// Create the actor from the machine
			const wizardActor = stateRegistry.registerMachine('wizardMachine', wizardMachine);

			// Move forward
			wizardActor.send({ type: 'NEXT' });
			expect(wizardActor.getSnapshot().value).toBe('step2');

			// Move backward
			wizardActor.send({ type: 'PREV' });
			expect(wizardActor.getSnapshot().value).toBe('step1');

			// Move forward twice
			wizardActor.send({ type: 'NEXT' });
			wizardActor.send({ type: 'NEXT' });
			expect(wizardActor.getSnapshot().value).toBe('step3');

			// Move backward and forward again
			wizardActor.send({ type: 'PREV' });
			expect(wizardActor.getSnapshot().value).toBe('step2');
			wizardActor.send({ type: 'NEXT' });
			expect(wizardActor.getSnapshot().value).toBe('step3');
		});
	});
});
