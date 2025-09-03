/*
 * Machine Logger (rewritten 2025-04-28, rev C)
 * ------------------------------------------------
 * XState inspector with rich logging + perf tracking
 * - Type-safe option merge (TS18048 & TS2339 fixed)
 */

import {
	type AnyStateMachine,
	type InspectionEvent,
	type InspectedEventEvent,
	type InspectedSnapshotEvent,
	type InspectedActorEvent,
	type Actor,
	type ActorOptions
} from 'xstate';
import { logger } from './logger';
import { LogLevel, type MachineLoggerOptions } from './types';
import { createStateContext } from './context';
import { loggingConfig } from '$lib/config/logging';

/**
 * Default options.
 */
const DEFAULT_MACHINE_LOGGER_OPTIONS: MachineLoggerOptions = {
	name: 'unnamed-machine',
	level: LogLevel.INFO,
	includedEvents: [],
	excludedEvents: [],
	contextFields: [],
	includeSnapshots: false,
	logTransitions: loggingConfig.machineLogging.logTransitions,
	performanceTracking: {
		enabled: loggingConfig.machineLogging.performanceTracking.enabled,
		transitionThreshold: loggingConfig.machineLogging.performanceTracking.transitionThreshold
	}
};

/* ----------------------------------------------------------------------------
 * Internal trackers
 * ------------------------------------------------------------------------- */
const transitionStartTimes = new Map<string, number>();
const previousStates = new Map<string, any>();

/* ----------------------------------------------------------------------------
 * Option merger – strictly typed, no {} property errors
 * ------------------------------------------------------------------------- */
function mergeOptions(partial: Partial<MachineLoggerOptions>): MachineLoggerOptions {
	const defaultPerf = DEFAULT_MACHINE_LOGGER_OPTIONS.performanceTracking!;

	return {
		...DEFAULT_MACHINE_LOGGER_OPTIONS,
		...partial,
		performanceTracking: {
			enabled: partial.performanceTracking?.enabled ?? defaultPerf.enabled,
			transitionThreshold:
				partial.performanceTracking?.transitionThreshold ?? defaultPerf.transitionThreshold
		}
	};
}

/* ----------------------------------------------------------------------------
 * createMachineInspector
 * ------------------------------------------------------------------------- */
export function createMachineInspector(
	machineId: string,
	options: Partial<MachineLoggerOptions> = {}
): (inspectionEvent: InspectionEvent) => void {
	const config = mergeOptions({ ...options, name: options.name ?? machineId });

	const machineLogger = logger.createChildLogger(
		config.name || machineId,
		createStateContext({ machine: machineId })
	);

	return (inspectionEvent: InspectionEvent) => {
		if (!inspectionEvent.type) return;

		switch (inspectionEvent.type) {
			/* -------------------- @xstate.event -------------------- */
			case '@xstate.event': {
				const evt = inspectionEvent as InspectedEventEvent;
				const t = evt.event.type;

				if (t === 'xstate.init') {
					machineLogger.info('Machine initialized', { data: { machineId } });
				} else if (t === 'xstate.stop') {
					machineLogger.info('Machine stopped', { data: { machineId } });
					transitionStartTimes.delete(machineId);
					previousStates.delete(machineId);
				}

				handleEventInspection(machineId, evt, machineLogger, config);
				break;
			}

			/* -------------------- @xstate.snapshot ----------------- */
			case '@xstate.snapshot':
				handleSnapshotInspection(
					machineId,
					inspectionEvent as InspectedSnapshotEvent,
					machineLogger,
					config
				);
				break;

			/* -------------------- @xstate.actor -------------------- */
			case '@xstate.actor': {
				const actorEvt = inspectionEvent as InspectedActorEvent;
				machineLogger.debug('Actor event', { data: { actorRef: actorEvt.actorRef } });
				break;
			}
		}
	};
}

/* ----------------------------------------------------------------------------
 * Event inspection
 * ------------------------------------------------------------------------- */
function handleEventInspection(
	machineId: string,
	inspectionEvent: InspectedEventEvent,
	machineLogger: any,
	options: MachineLoggerOptions
): void {
	const eventType = inspectionEvent.event.type;
	const isInternal =
		eventType.startsWith('xstate.') ||
		eventType.startsWith('done.') ||
		eventType.startsWith('error.');

	if (isInternal && !options.includedEvents?.includes(eventType)) return;
	if (options.excludedEvents?.includes(eventType)) return;

	if (options.performanceTracking?.enabled) {
		transitionStartTimes.set(machineId, performance.now());
	}

	machineLogger.debug(`Event: ${eventType}`, {
		data: { event: inspectionEvent, payload: inspectionEvent.event }
	});
}

/* ----------------------------------------------------------------------------
 * Snapshot inspection
 * ------------------------------------------------------------------------- */
function handleSnapshotInspection(
	machineId: string,
	inspectionEvent: InspectedSnapshotEvent,
	machineLogger: any,
	options: MachineLoggerOptions
): void {
	const snapshot = inspectionEvent.snapshot;
	const currentState = 'value' in snapshot ? snapshot.value : snapshot.status;
	const prev = previousStates.get(machineId);

	if (prev && JSON.stringify(prev) === JSON.stringify(currentState)) return;

	let duration: number | undefined;
	if (options.performanceTracking?.enabled) {
		const start = transitionStartTimes.get(machineId);
		if (start) {
			duration = performance.now() - start;
			transitionStartTimes.delete(machineId);
		}
	}

	if (options.logTransitions) {
		const contextData: Record<string, unknown> = {};
		const ctx = 'context' in snapshot ? snapshot.context : undefined;

		if (ctx && options.contextFields?.length) {
			for (const field of options.contextFields) {
				if (field in (ctx as Record<string, unknown>)) {
					contextData[field] = (ctx as Record<string, unknown>)[field];
				}
			}
		}

		const slow =
			duration !== undefined && duration > (options.performanceTracking?.transitionThreshold ?? 50);
		const level = slow ? LogLevel.WARN : LogLevel.INFO;

		machineLogger.log(level, `State: ${JSON.stringify(currentState)}`, {
			data: {
				from: prev ? JSON.stringify(prev) : 'initial',
				to: JSON.stringify(currentState),
				context: Object.keys(contextData).length ? contextData : undefined,
				snapshot: options.includeSnapshots ? snapshot : undefined
			},
			duration
		});

		if (slow && duration) {
			machineLogger.warn(`Slow transition (${duration.toFixed(2)}ms)`, {
				data: {
					threshold: options.performanceTracking?.transitionThreshold,
					machineId,
					from: prev,
					to: currentState
				},
				duration
			});
		}
	}

	previousStates.set(machineId, currentState);
}

/* ----------------------------------------------------------------------------
 * Higher-order helpers
 * ------------------------------------------------------------------------- */
export function withLogging<T extends AnyStateMachine>(
	machine: T,
	opts?: Partial<MachineLoggerOptions>
): T {
	return {
		...machine,
		__logging: true,
		__loggingOptions: opts
	} as T;
}

export function createLoggedActor<T extends AnyStateMachine>(
	machine: T,
	options: {
		id?: string;
		logging?: Partial<MachineLoggerOptions>;
		snapshot?: any;
	} = {}
): Actor<T> {
	const machineId = options.id || machine.id || `machine-${Date.now()}`;
	const stored = (machine as any).__loggingOptions as Partial<MachineLoggerOptions> | undefined;

	const loggingOptions = mergeOptions({
		name: machineId,
		...(stored || {}),
		...(options.logging || {})
	});

	const inspector = createMachineInspector(machineId, loggingOptions);
	const actorOptions: ActorOptions<T> = {
		id: machineId,
		snapshot: options.snapshot,
		inspect: inspector
	};

	const actor = createActor(machine, actorOptions);
	actor.start();
	return actor;
}

// late import to dodge circular dep
import { createActor } from 'xstate';
