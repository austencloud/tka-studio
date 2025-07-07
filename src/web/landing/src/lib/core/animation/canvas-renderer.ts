// Canvas rendering utilities for the pictograph animator

import type { PropState, CanvasState } from "./types";
import {
  CANVAS_SIZE,
  GRID_VIEWBOX_SIZE,
  GRID_HALFWAY_POINT_OFFSET,
  STAFF_VIEWBOX_WIDTH,
  STAFF_VIEWBOX_HEIGHT,
  STAFF_CENTER_X,
  STAFF_CENTER_Y,
  gridSvgString,
  staffBaseSvgString,
} from "./constants";

const gridScaleFactor = CANVAS_SIZE / GRID_VIEWBOX_SIZE;
const scaledHalfwayRadius = GRID_HALFWAY_POINT_OFFSET * gridScaleFactor;

// Image loading utilities
export function loadImage(svgString: string): Promise<HTMLImageElement> {
  console.log(
    "🖼️ IMAGE: Loading image from SVG (" + svgString.length + " chars)"
  );
  return new Promise((resolve, reject) => {
    const img = new Image();
    const svgBlob = new Blob([svgString], {
      type: "image/svg+xml;charset=utf-8",
    });
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
      console.log(
        "✅ IMAGE: Loaded successfully:",
        img.width + "x" + img.height
      );
      URL.revokeObjectURL(url);
      resolve(img);
    };

    img.onerror = (e) => {
      console.error("❌ IMAGE: Load error:", e);
      URL.revokeObjectURL(url);
      reject(new Error("Image load error: " + e));
    };

    img.src = url;
    console.log("🖼️ IMAGE: Created blob URL:", url);
  });
}

export async function loadAllImages(): Promise<{
  gridImage: HTMLImageElement;
  blueStaffImage: HTMLImageElement;
  redStaffImage: HTMLImageElement;
}> {
  console.log("🖼️ IMAGES: Starting to load images...");
  console.log("🖼️ IMAGES: Grid SVG length:", gridSvgString.length);
  console.log(
    "🖼️ IMAGES: Staff SVG template ready:",
    typeof staffBaseSvgString
  );

  const [gridImage, blueStaffImage, redStaffImage] = await Promise.all([
    loadImage(gridSvgString),
    loadImage(staffBaseSvgString("#2E3192")),
    loadImage(staffBaseSvgString("#ED1C24")),
  ]);

  console.log("✅ IMAGES: All images loaded successfully!");
  console.log(
    "🖼️ IMAGES: Grid image dimensions:",
    gridImage.width,
    "x",
    gridImage.height
  );
  console.log(
    "🖼️ IMAGES: Blue staff dimensions:",
    blueStaffImage.width,
    "x",
    blueStaffImage.height
  );
  console.log(
    "🖼️ IMAGES: Red staff dimensions:",
    redStaffImage.width,
    "x",
    redStaffImage.height
  );

  return { gridImage, blueStaffImage, redStaffImage };
}

// Drawing functions
export function drawGrid(
  ctx: CanvasRenderingContext2D,
  gridImage: HTMLImageElement
): void {
  console.log("🗺️ GRID: Drawing grid...");
  try {
    console.log(
      "🗺️ GRID: Drawing image at 0,0 with size",
      CANVAS_SIZE,
      "x",
      CANVAS_SIZE
    );
    ctx.drawImage(gridImage, 0, 0, CANVAS_SIZE, CANVAS_SIZE);
    console.log("✅ GRID: Drawn successfully!");
  } catch (error) {
    console.error("❌ GRID: Error drawing:", error);
  }
}

export function drawStaff(
  ctx: CanvasRenderingContext2D,
  propState: PropState,
  staffImage: HTMLImageElement
): void {
  if (!propState) return;

  const centerX = CANVAS_SIZE / 2;
  const centerY = CANVAS_SIZE / 2;
  const inwardFactor = 0.95;
  const x =
    centerX +
    Math.cos(propState.centerPathAngle) * scaledHalfwayRadius * inwardFactor;
  const y =
    centerY +
    Math.sin(propState.centerPathAngle) * scaledHalfwayRadius * inwardFactor;

  const staffWidth = STAFF_VIEWBOX_WIDTH * gridScaleFactor;
  const staffHeight = STAFF_VIEWBOX_HEIGHT * gridScaleFactor;

  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(propState.staffRotationAngle);
  ctx.drawImage(
    staffImage,
    -STAFF_CENTER_X * gridScaleFactor,
    -STAFF_CENTER_Y * gridScaleFactor,
    staffWidth,
    staffHeight
  );
  ctx.restore();
}

export function render(
  canvasState: CanvasState,
  bluePropState: PropState,
  redPropState: PropState
): void {
  console.log("🎨 RENDER: Starting render...", {
    ctx: !!canvasState.ctx,
    imagesLoaded: canvasState.imagesLoaded,
  });
  if (
    !canvasState.ctx ||
    !canvasState.imagesLoaded ||
    !canvasState.gridImage ||
    !canvasState.blueStaffImage ||
    !canvasState.redStaffImage
  ) {
    console.log("⚠️ RENDER: Skipped - missing requirements");
    return;
  }

  console.log("🎨 RENDER: Clearing canvas...");
  canvasState.ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  console.log("🎨 RENDER: Drawing grid...");
  drawGrid(canvasState.ctx, canvasState.gridImage);
  console.log("🎨 RENDER: Drawing blue staff...");
  drawStaff(canvasState.ctx, bluePropState, canvasState.blueStaffImage);
  console.log("🎨 RENDER: Drawing red staff...");
  drawStaff(canvasState.ctx, redPropState, canvasState.redStaffImage);
  console.log("✅ RENDER: Complete!");
}

export function drawErrorMessage(
  ctx: CanvasRenderingContext2D,
  message: string
): void {
  if (!ctx) return;
  ctx.fillStyle = "#dc2626";
  ctx.font = "16px Arial";
  ctx.textAlign = "center";
  ctx.fillText("Error loading images.", CANVAS_SIZE / 2, CANVAS_SIZE / 2);
  ctx.fillText(
    "Please refresh the page.",
    CANVAS_SIZE / 2,
    CANVAS_SIZE / 2 + 25
  );
}

export function drawLoadingMessage(ctx: CanvasRenderingContext2D): void {
  if (!ctx) return;
  ctx.fillStyle = "#e5e7eb";
  ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  ctx.fillStyle = "#1f2937";
  ctx.font = "16px Arial";
  ctx.textAlign = "center";
  ctx.fillText("Loading animation assets...", CANVAS_SIZE / 2, CANVAS_SIZE / 2);
}
