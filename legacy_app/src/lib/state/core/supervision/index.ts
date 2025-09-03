// src/lib/state/core/supervision/index.ts
/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */
export * from './types'; // <- keeps the interfaces

/* -------------------------------------------------------------------------- */
/*  Runtime implementations                                                   */
/* -------------------------------------------------------------------------- */
export * from './strategies';
export * from './CircuitBreaker';

// give the classes unique names so they don’t collide with the interfaces
export { SupervisedActor as SupervisedActorClass } from './SupervisedActor';
export { Supervisor as SupervisorClass } from './Supervisor';
export { RootSupervisor } from './RootSupervisor';
