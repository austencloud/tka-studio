// Background modules - clean modular structure
export * from "./aurora";
export * from "./deep-ocean";
export * from "./night-sky";
export * from "./shared";
export * from "./simple";
export * from "./snowfall";

// Export BackgroundType and BackgroundCategory enums
export {
  BackgroundCategory,
  BackgroundType,
} from "./shared/domain/enums/background-enums";

// Export specific types that are needed across modules
export type {
  Bubble,
  DeepOceanState,
  MarineLife,
  OceanParticle,
} from "./deep-ocean/domain/models/DeepOceanModels";
export { updateBodyBackground } from "./shared/background-preloader";
export type {
  ShootingStar,
  ShootingStarState,
  Snowflake,
} from "./snowfall/domain/models/snowfall-models";
