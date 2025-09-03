/**
 * Dependency management utilities for the state registry
 */

/**
 * Add a dependency relationship between state containers
 */
export function addDependency(
  dependencies: Map<string, Set<string>>,
  containerExists: (id: string) => boolean,
  dependentId: string,
  dependencyId: string
): boolean {
  // Check if both IDs exist in the registry
  if (!containerExists(dependentId)) {
    // Use debug level instead of warn to reduce console noise during initialization
    // This is expected during initialization when actors are being registered
    console.debug(`Cannot add dependency: dependent ID "${dependentId}" is not registered`);
    return false;
  }
  if (!containerExists(dependencyId)) {
    console.debug(`Cannot add dependency: dependency ID "${dependencyId}" is not registered`);
    return false;
  }

  // Get or create the set of dependencies for this dependent
  if (!dependencies.has(dependentId)) {
    dependencies.set(dependentId, new Set());
  }

  // Add the dependency
  dependencies.get(dependentId)!.add(dependencyId);
  return true;
}

/**
 * Get all dependencies for a state container
 */
export function getDependencies(dependencies: Map<string, Set<string>>, id: string): string[] {
  return Array.from(dependencies.get(id) || []);
}

/**
 * Get all dependents of a state container
 */
export function getDependents(dependencies: Map<string, Set<string>>, id: string): string[] {
  const dependents: string[] = [];
  dependencies.forEach((deps, depId) => {
    if (deps.has(id)) {
      dependents.push(depId);
    }
  });
  return dependents;
}

/**
 * Perform topological sorting of the dependency graph
 * This ensures that dependencies are initialized before dependents
 */
export function topologicalSort(
  dependencies: Map<string, Set<string>>,
  containerIds: string[]
): string[] {
  const result: string[] = [];
  const visited = new Set<string>();
  const temporaryMark = new Set<string>();

  // Helper function for depth-first search
  const visit = (id: string) => {
    if (temporaryMark.has(id)) {
      console.error(`Circular dependency detected including ${id}`);
      return; // Skip circular dependencies
    }
    if (visited.has(id)) return;

    temporaryMark.add(id);

    // Visit all dependencies first
    const deps = dependencies.get(id);
    if (deps) {
      for (const depId of deps) {
        visit(depId);
      }
    }

    temporaryMark.delete(id);
    visited.add(id);
    result.push(id);
  };

  // Visit all nodes
  for (const id of containerIds) {
    if (!visited.has(id)) {
      visit(id);
    }
  }

  return result;
}
