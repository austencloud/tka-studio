import type { SupervisionStrategyPlugin, StrategyRegistry, SupervisionStrategy } from './types';

class StrategyRegistryImpl implements StrategyRegistry {
	private plugins = new Map<string, SupervisionStrategyPlugin>();

	register<TConfig>(plugin: SupervisionStrategyPlugin<TConfig>): void {
		if (this.plugins.has(plugin.type)) {
			throw new Error(`Strategy plugin "${plugin.type}" is already registered`);
		}
		this.plugins.set(plugin.type, plugin);
	}

	unregister(type: string): void {
		this.plugins.delete(type);
	}

	get(type: string): SupervisionStrategyPlugin | undefined {
		return this.plugins.get(type);
	}

	create<TConfig>(type: string, config?: Partial<TConfig>): SupervisionStrategy {
		const plugin = this.plugins.get(type) as SupervisionStrategyPlugin<TConfig>;
		if (!plugin) {
			throw new Error(`No strategy plugin found for type "${type}"`);
		}
		return plugin.createStrategy(config);
	}
}

// Export singleton instance
export const strategyRegistry = new StrategyRegistryImpl();
