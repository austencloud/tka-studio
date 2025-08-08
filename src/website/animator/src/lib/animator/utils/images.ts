// utils/images.ts - Image loading and rendering utilities
const GRID_SVG_STRING = `<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 950 950" style="enable-background:new 0 0 950 950; background-color: #ffffff;" xml:space="preserve"><g id="outer_points"><circle fill="#000000" cx="475" cy="175" r="25"/><circle fill="#000000" cx="775" cy="475" r="25"/><circle fill="#000000" cx="475" cy="775" r="25"/><circle fill="#000000" cx="175" cy="475" r="25"/></g><g id="halfway_points"><circle fill="#000000" cx="475" cy="323.5" r="8"/><circle fill="#000000" cx="626.5" cy="475" r="8"/><circle fill="#000000" cx="475" cy="626.5" r="8"/><circle fill="#000000" cx="323.5" cy="475" r="8"/></g><g id="center_group"><circle fill="#000000" cx="475" cy="475" r="12"/></g></svg>`;

const STAFF_BASE_SVG_STRING = (fillColor: string) =>
  `<svg version="1.1" id="staff" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 252.8 77.8" style="enable-background:new 0 0 252.8 77.8;" xml:space="preserve"><path fill="${fillColor}" stroke="#555555" stroke-width="1" stroke-miterlimit="10" d="M251.4,67.7V10.1c0-4.8-4.1-8.7-9.1-8.7s-9.1,3.9-9.1,8.7v19.2H10.3c-4.9,0-8.9,3.8-8.9,8.5V41 c0,4.6,4,8.5,8.9,8.5h222.9v18.2c0,4.8,4.1,8.7,9.1,8.7S251.4,72.5,251.4,67.7z"/><circle id="centerPoint" fill="#FF0000" cx="126.4" cy="38.9" r="5" /></svg>`;

// Constants from HTML
const GRID_VIEWBOX_SIZE = 950;
const GRID_CENTER = GRID_VIEWBOX_SIZE / 2;
const GRID_HALFWAY_POINT_OFFSET = 151.5;
const STAFF_VIEWBOX_WIDTH = 252.8;
const STAFF_VIEWBOX_HEIGHT = 77.8;
const STAFF_CENTER_X = 126.4;
const STAFF_CENTER_Y = 38.9;

export function loadImage(svgString: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const svgBlob = new Blob([svgString], {
      type: "image/svg+xml;charset=utf-8",
    });
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {
      URL.revokeObjectURL(url);
      resolve(img);
    };

    img.onerror = (e) => {
      URL.revokeObjectURL(url);
      reject(new Error("Image load error"));
    };

    img.src = url;
  });
}

export async function loadAllImages(): Promise<{
  gridImage: HTMLImageElement;
  blueStaffImage: HTMLImageElement;
  redStaffImage: HTMLImageElement;
}> {
  const [gridImage, blueStaffImage, redStaffImage] = await Promise.all([
    loadImage(GRID_SVG_STRING),
    loadImage(STAFF_BASE_SVG_STRING("#2E3192")),
    loadImage(STAFF_BASE_SVG_STRING("#ED1C24")),
  ]);

  return { gridImage, blueStaffImage, redStaffImage };
}

export function drawGrid(
  ctx: CanvasRenderingContext2D,
  gridImage: HTMLImageElement,
  canvasSize: number
): void {
  ctx.drawImage(gridImage, 0, 0, canvasSize, canvasSize);
}

export function drawStaff(
  ctx: CanvasRenderingContext2D,
  staffImage: HTMLImageElement,
  centerPathAngle: number,
  staffRotationAngle: number,
  canvasSize: number
): void {
  const centerX = canvasSize / 2;
  const centerY = canvasSize / 2;
  const gridScaleFactor = canvasSize / GRID_VIEWBOX_SIZE;
  const scaledHalfwayRadius = GRID_HALFWAY_POINT_OFFSET * gridScaleFactor;
  const inwardFactor = 0.95;

  const x =
    centerX + Math.cos(centerPathAngle) * scaledHalfwayRadius * inwardFactor;
  const y =
    centerY + Math.sin(centerPathAngle) * scaledHalfwayRadius * inwardFactor;

  const staffWidth = STAFF_VIEWBOX_WIDTH * gridScaleFactor;
  const staffHeight = STAFF_VIEWBOX_HEIGHT * gridScaleFactor;

  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(staffRotationAngle);
  ctx.drawImage(
    staffImage,
    -STAFF_CENTER_X * gridScaleFactor,
    -STAFF_CENTER_Y * gridScaleFactor,
    staffWidth,
    staffHeight
  );
  ctx.restore();
}
