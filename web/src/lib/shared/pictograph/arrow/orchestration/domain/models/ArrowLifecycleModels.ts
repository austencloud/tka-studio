/**
 * Arrow Lifecycle Domain Models
 *
 * Domain models for arrow lifecycle management.
 * Pure data structures with no business logic.
 */

export interface ArrowAssets {
  readonly imageSrc: string;
  readonly viewBox: { width: number; height: number };
  readonly center: { x: number; y: number };
}

export interface ArrowPosition {
  readonly x: number;
  readonly y: number;
  readonly rotation: number;
}

export interface ArrowState {
  readonly assets: ArrowAssets | null;
  readonly position: ArrowPosition | null;
  readonly shouldMirror: boolean;
  readonly isVisible: boolean;
  readonly isLoading: boolean;
  readonly error: string | null;
}

export interface ArrowLifecycleResult {
  readonly positions: Record<string, ArrowPosition>;
  readonly mirroring: Record<string, boolean>;
  readonly assets: Record<string, ArrowAssets>;
  readonly allReady: boolean;
  readonly errors: Record<string, string>;
}

export function createArrowAssets(data: Partial<ArrowAssets>): ArrowAssets {
  return {
    imageSrc: data.imageSrc ?? '',
    viewBox: data.viewBox ?? { width: 0, height: 0 },
    center: data.center ?? { x: 0, y: 0 },
  };
}

export function createArrowPosition(data: Partial<ArrowPosition>): ArrowPosition {
  return {
    x: data.x ?? 0,
    y: data.y ?? 0,
    rotation: data.rotation ?? 0,
  };
}

export function createArrowState(data: Partial<ArrowState> = {}): ArrowState {
  return {
    assets: data.assets ?? null,
    position: data.position ?? null,
    shouldMirror: data.shouldMirror ?? false,
    isVisible: data.isVisible ?? false,
    isLoading: data.isLoading ?? false,
    error: data.error ?? null,
  };
}

export function createArrowLifecycleResult(data: Partial<ArrowLifecycleResult> = {}): ArrowLifecycleResult {
  return {
    positions: data.positions ?? {},
    mirroring: data.mirroring ?? {},
    assets: data.assets ?? {},
    allReady: data.allReady ?? false,
    errors: data.errors ?? {},
  };
}
