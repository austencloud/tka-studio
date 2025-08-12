import type { ResourceTracker as ResourceTrackerInterface } from '../types/types';

interface Disposable {
	dispose?(): void;
	close?(): void;
	cleanup?(): void;
}

type TrackedResource =
	| HTMLElement
	| HTMLImageElement
	| HTMLCanvasElement
	| Worker
	| WebGLRenderingContext
	| WebGL2RenderingContext
	| Path2D
	| Disposable
	| TrackedResource[]
	| Set<TrackedResource>
	| Map<unknown, TrackedResource>
	| unknown;

export class ResourceTracker implements ResourceTrackerInterface {
	private resources: Set<TrackedResource>;
	private isActive: boolean;

	constructor() {
		this.resources = new Set();
		this.isActive = true;
	}

	public trackResource<T>(resource: T): T {
		if (!this.isActive) {
			console.warn('Attempting to track a resource after ResourceTracker has been disposed');
			return resource;
		}

		this.resources.add(resource);
		return resource;
	}

	public untrackResource(resource: TrackedResource): void {
		this.resources.delete(resource);
	}

	public disposeAll(): void {
		if (!this.isActive) return;

		try {
			this.resources.forEach((resource) => {
				this.disposeResource(resource);
			});

			this.resources.clear();
		} catch (e) {
			console.error('Error disposing resources:', e);
		} finally {
			this.isActive = false;
		}
	}

	private disposeResource(resource: TrackedResource): void {
		if (!resource) return;

		if (resource instanceof HTMLElement) {
			if (resource.parentNode) {
				resource.parentNode.removeChild(resource);
			}

			if (resource instanceof HTMLImageElement) {
				resource.onload = null;
				resource.onerror = null;

				resource.src = '';
			} else if (resource instanceof HTMLCanvasElement) {
				const context = resource.getContext('2d');
				if (context) {
					context.setTransform(1, 0, 0, 1, 0, 0);
					context.clearRect(0, 0, resource.width, resource.height);
				}
			}
		} else if (
			resource instanceof WebGLRenderingContext ||
			resource instanceof WebGL2RenderingContext
		) {
			const extension = resource.getExtension('WEBGL_lose_context');
			if (extension) extension.loseContext();
		} else if (resource instanceof Path2D) {
			// Path2D objects don't need explicit cleanup
		} else if (
			resource &&
			typeof resource === 'object' &&
			'dispose' in resource &&
			typeof resource.dispose === 'function'
		) {
			resource.dispose();
		} else if (
			resource &&
			typeof resource === 'object' &&
			'close' in resource &&
			typeof resource.close === 'function'
		) {
			resource.close();
		} else if (
			resource &&
			typeof resource === 'object' &&
			'cleanup' in resource &&
			typeof resource.cleanup === 'function'
		) {
			resource.cleanup();
		} else if (Array.isArray(resource)) {
			resource.forEach((item) => this.disposeResource(item));
		} else if (resource instanceof Set || resource instanceof Map) {
			resource.forEach((item) => this.disposeResource(item));
			resource.clear();
		}
	}

	public isTracking(resource: TrackedResource): boolean {
		return this.resources.has(resource);
	}

	public get resourceCount(): number {
		return this.resources.size;
	}
}

export function createResourceTracker(): ResourceTracker {
	return new ResourceTracker();
}
