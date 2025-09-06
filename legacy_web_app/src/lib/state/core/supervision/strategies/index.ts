import { strategyRegistry } from '../StrategyRegistry';
import { RestartPlugin } from './RestartPlugin';
import { StopPlugin } from './StopPlugin';
import { EscalatePlugin } from './EscalatePlugin';
import { ResumePlugin } from './ResumePlugin';

// Register built-in strategies
strategyRegistry.register(RestartPlugin);
strategyRegistry.register(StopPlugin);
strategyRegistry.register(EscalatePlugin);
strategyRegistry.register(ResumePlugin);

// Re-export strategy classes and plugins
export * from './RestartStrategy';
export * from './StopStrategy';
export * from './EscalateStrategy';
export * from './ResumeStrategy';

export { RestartPlugin, StopPlugin, EscalatePlugin, ResumePlugin };

// Export the registry for plugin management
export { strategyRegistry };
