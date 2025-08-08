import { strategyRegistry } from '../StrategyRegistry.js';
import { RestartPlugin } from './RestartPlugin.js';
import { StopPlugin } from './StopPlugin.js';
import { EscalatePlugin } from './EscalatePlugin.js';
import { ResumePlugin } from './ResumePlugin.js';

// Register built-in strategies
strategyRegistry.register(RestartPlugin);
strategyRegistry.register(StopPlugin);
strategyRegistry.register(EscalatePlugin);
strategyRegistry.register(ResumePlugin);

// Re-export strategy classes and plugins
export * from './RestartStrategy.js';
export * from './StopStrategy.js';
export * from './EscalateStrategy.js';
export * from './ResumeStrategy.js';

export { RestartPlugin, StopPlugin, EscalatePlugin, ResumePlugin };

// Export the registry for plugin management
export { strategyRegistry };
