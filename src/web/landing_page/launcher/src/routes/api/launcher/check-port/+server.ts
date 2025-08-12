import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { createServer } from "net";

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { port } = await request.json();

    if (!port || typeof port !== "number") {
      return json({ available: false, error: "Invalid port" }, { status: 400 });
    }

    const available = await checkPortAvailability(port);

    return json({ available, port });
  } catch (error) {
    console.error("Port check error:", error);
    return json(
      {
        available: false,
        error: "Failed to check port",
      },
      { status: 500 },
    );
  }
};

function checkPortAvailability(port: number): Promise<boolean> {
  return new Promise((resolve) => {
    const server = createServer();

    server.listen(port, () => {
      server.close(() => {
        resolve(true);
      });
    });

    server.on("error", () => {
      resolve(false);
    });
  });
}
