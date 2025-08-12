/**
 * 🏭 TKA APPLICATION FACTORY
 *
 * Simplified application factory for the landing project.
 * Creates basic dependency injection containers for pictograph rendering.
 */

// ============================================================================
// SIMPLE SERVICE CONTAINER
// ============================================================================

class SimpleServiceContainer {
  private services = new Map<string, any>();
  private singletons = new Map<string, any>();

  registerSingleton<T>(token: string, implementation: new (...args: any[]) => T): void {
    this.services.set(token, { implementation, scope: 'singleton' });
  }

  resolve<T>(token: string): T {
    if (this.singletons.has(token)) {
      return this.singletons.get(token);
    }

    const service = this.services.get(token);
    if (!service) {
      throw new Error(`Service not found: ${token}`);
    }

    const instance = new service.implementation();
    
    if (service.scope === 'singleton') {
      this.singletons.set(token, instance);
    }

    return instance;
  }
}

// ============================================================================
// MOCK IMPLEMENTATIONS
// ============================================================================

class MockPictographRenderer {
  async renderPictograph(data: any): Promise<SVGElement> {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', '300');
    svg.setAttribute('height', '300');
    svg.setAttribute('viewBox', '0 0 950 950');
    
    // Add a simple placeholder
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', '50');
    rect.setAttribute('y', '50');
    rect.setAttribute('width', '850');
    rect.setAttribute('height', '850');
    rect.setAttribute('fill', 'none');
    rect.setAttribute('stroke', '#ccc');
    rect.setAttribute('stroke-width', '2');
    svg.appendChild(rect);

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', '475');
    text.setAttribute('y', '475');
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', '#666');
    text.textContent = 'Pictograph Placeholder';
    svg.appendChild(text);

    return svg;
  }

  setVisibility(options: any): void {
    // Mock implementation
  }
}

class MockPictographOrchestrator {
  createPictograph(): any {
    return {
      id: 'mock-pictograph',
      name: 'Mock Pictograph',
      // Add other mock properties as needed
    };
  }
}

// ============================================================================
// APPLICATION FACTORY
// ============================================================================

export class ApplicationFactory {
  static createProductionApp(): SimpleServiceContainer {
    const container = new SimpleServiceContainer();

    // Register mock services
    container.registerSingleton('IPictographRenderer', MockPictographRenderer);
    container.registerSingleton('IPictographOrchestrator', MockPictographOrchestrator);

    return container;
  }

  // Additional factory methods can be added as needed
  static createTestApp(): SimpleServiceContainer {
    return this.createProductionApp();
  }

  static createDevelopmentApp(): SimpleServiceContainer {
    return this.createProductionApp();
  }
}