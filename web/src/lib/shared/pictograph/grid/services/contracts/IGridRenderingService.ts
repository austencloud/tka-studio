import type { GridMode } from "../../domain";

export interface IGridRenderingService {
  renderGrid(svg: SVGElement, gridMode?: GridMode): Promise<void>;
}