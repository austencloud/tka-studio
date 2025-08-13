import { json } from "@sveltejs/kit";
const POST = async ({ request }) => {
  try {
    const { level, message, timestamp } = await request.json();
    const formattedMessage = `[BROWSER-${level}] ${timestamp} ${message}`;
    switch (level) {
      case "ERROR":
        console.error(formattedMessage);
        break;
      case "WARN":
        console.warn(formattedMessage);
        break;
      default:
        console.log(formattedMessage);
        break;
    }
    return json({ success: true });
  } catch (error) {
    console.error("[SERVER] Failed to log browser message:", error);
    return json({ success: false }, { status: 500 });
  }
};
export {
  POST
};
