<!-- Import at the end to avoid circular dependencies -->
<script context="module" lang="ts">
	import { getContext } from 'svelte';
</script>

<!--
  Logging Provider Component

  Provides logging context to Svelte components and initializes the logging system.
-->
<script lang="ts">
	import { setContext, onMount, onDestroy } from 'svelte';
	import { writable, type Writable } from 'svelte/store';
	import {
		logger,
		type Logger,
		type ComponentLoggerOptions,
		LogDomain,
		createComponentContext,
		MemoryTransport
	} from '$lib/core/logging';

	// Props
	export let name: string = 'app';
	export let options: ComponentLoggerOptions = {
		enableTiming: true,
		trackLifecycle: true,
		trackRenders: false,
		trackErrors: true
	};

	// Context key for the logger
	const LOGGER_CONTEXT_KEY = Symbol('logger');

	// Create a memory transport for the debug panel
	const memoryTransport = new MemoryTransport();

	// Add the memory transport to the logger
	logger.setConfig({
		transports: [memoryTransport]
	});

	// Create a component logger
	const componentLogger = logger.createChildLogger(
		name,
		createComponentContext({
			component: name,
			props: $$props
		})
	);

	// Create a store for the logs
	const logs = writable<any[]>([]);

	// Subscribe to memory transport logs
	const unsubscribe = memoryTransport.addListener((entries) => {
		logs.set(entries);
	});

	// Track render count
	let renderCount = 0;

	// Track component lifecycle
	onMount(() => {
		renderCount++;

		if (options.trackLifecycle) {
			componentLogger.info(`Component mounted: ${name}`, {
				domain: LogDomain.COMPONENT,
				data: {
					renderCount,
					props: $$props
				}
			});
		}

		// Track errors in the component
		if (options.trackErrors) {
			const errorHandler = (event: ErrorEvent) => {
				// Check if the error occurred in this component
				// This is a simplistic check and might need refinement
				if (event.filename && event.filename.includes(name)) {
					componentLogger.error(`Error in component: ${name}`, {
						domain: LogDomain.COMPONENT,
						error: {
							message: event.message,
							stack: event.error?.stack
						},
						data: {
							filename: event.filename,
							lineno: event.lineno,
							colno: event.colno
						}
					});
				}
			};

			window.addEventListener('error', errorHandler);

			return () => {
				window.removeEventListener('error', errorHandler);
			};
		}
	});

	onDestroy(() => {
		if (options.trackLifecycle) {
			componentLogger.info(`Component destroyed: ${name}`, {
				domain: LogDomain.COMPONENT,
				data: {
					renderCount,
					lifetime: Date.now() - (componentLogger.getConfig()?.startTime || 0)
				}
			});
		}

		// Unsubscribe from memory transport
		unsubscribe();
	});

	// Set the logger in the context
	setContext(LOGGER_CONTEXT_KEY, {
		logger: componentLogger,
		logs,
		options
	});

	// Export the useLogger function for components to use
	export function useLogger(
		componentName: string,
		componentOptions: ComponentLoggerOptions = {}
	): Logger {
		const contextLogger = getContext<{
			logger: Logger;
			logs: Writable<any[]>;
			options: ComponentLoggerOptions;
		}>(LOGGER_CONTEXT_KEY);

		if (!contextLogger) {
			console.warn(`No logger context found. Make sure LoggingProvider is a parent component.`);
			return logger.createChildLogger(componentName);
		}

		// Create a child logger with the component name
		return contextLogger.logger.createChildLogger(
			componentName,
			createComponentContext({
				component: componentName,
				props: componentOptions.context
			})
		);
	}

	// Action to track performance of an element
	export function trackPerformance(
		node: HTMLElement,
		params: {
			elementName: string;
			trackRenders?: boolean;
		}
	) {
		const { elementName, trackRenders = false } = params;
		let renderTimer: any;

		// Use Intersection Observer to track when the element is visible
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						componentLogger.debug(`Element visible: ${elementName}`, {
							domain: LogDomain.COMPONENT,
							data: {
								elementName,
								visibleTime: Date.now(),
								intersectionRatio: entry.intersectionRatio
							}
						});
					}
				});
			},
			{
				threshold: [0, 0.5, 1]
			}
		);

		// Track render performance
		if (trackRenders) {
			const startRender = performance.now();

			renderTimer = setTimeout(() => {
				const renderTime = performance.now() - startRender;
				componentLogger.debug(`Element rendered: ${elementName}`, {
					domain: LogDomain.COMPONENT,
					duration: renderTime,
					data: {
						elementName,
						renderTime
					}
				});
			}, 0);
		}

		// Start observing
		observer.observe(node);

		return {
			update(newParams: { elementName: string; trackRenders?: boolean }) {
				// Update params if needed
			},
			destroy() {
				observer.disconnect();
				if (renderTimer) clearTimeout(renderTimer);
			}
		};
	}
</script>

<slot />
