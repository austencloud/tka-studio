// src/lib/state/core/supervision/index.ts
/* -------------------------------------------------------------------------- */
/*  Types                                                                     */
/* -------------------------------------------------------------------------- */
export * from './types.js'; // <- keeps the interfaces

/* -------------------------------------------------------------------------- */
/*  Runtime implementations                                                   */
/* -------------------------------------------------------------------------- */
export * from './strategies.js';
export * from './CircuitBreaker.js';

// give the classes unique names so they don’t collide with the interfaces
export { SupervisedActor as SupervisedActorClass } from './SupervisedActor.js';
export { Supervisor as SupervisorClass } from './Supervisor.js';
export { RootSupervisor } from './RootSupervisor.js';
