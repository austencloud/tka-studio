const handle = async ({ event, resolve }) => {
  if (event.url.pathname === "/api/console-forward") {
    if (event.request.method === "POST") {
      try {
        const body = await event.request.text();
        const data = JSON.parse(body);
        const timestamp = (/* @__PURE__ */ new Date()).toLocaleTimeString();
        const logLine = `[${timestamp}] BROWSER ${data.level}: ${data.message}`;
        process.stdout.write(logLine + "\n");
        return new Response("OK", { status: 200 });
      } catch {
        return new Response("Error", { status: 500 });
      }
    }
  }
  return resolve(event);
};
export {
  handle
};
