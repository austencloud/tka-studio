// import { getRedirectURL, shouldRedirectToPrimary } from "$config/domains"; // TODO: Fix config path
import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
  // Check if we need to redirect to primary domain
  // TODO: Restore domain redirect functionality
  // if (shouldRedirectToPrimary(event.url.origin)) {
  //   const redirectURL = getRedirectURL(event.url.href);
  //   return new Response(null, {
  //     status: 301, // Permanent redirect for SEO
  //     headers: {
  //       Location: redirectURL,
  //     },
  //   });
  // }

  // Handle console forwarding endpoint
  if (event.url.pathname === "/api/console-forward") {
    if (event.request.method === "POST") {
      try {
        const body = await event.request.text();
        const data = JSON.parse(body);

        // Write directly to stdout (terminal)
        const timestamp = new Date().toLocaleTimeString();
        const logLine = `[${timestamp}] BROWSER ${data.level}: ${data.message}`;
        process.stdout.write(logLine + "\n");

        return new Response("OK", { status: 200 });
      } catch {
        return new Response("Error", { status: 500 });
      }
    }
  }

  // Resolve the request with security headers
  const response = await resolve(event);

  // Set security headers for OAuth authentication flows
  // These headers allow OAuth popups (Google, Facebook, etc.) to properly communicate
  // with the parent window during authentication while maintaining security
  response.headers.set(
    "Cross-Origin-Opener-Policy",
    "same-origin-allow-popups"
  );

  // COEP header - allows cross-origin resources needed for OAuth
  response.headers.set("Cross-Origin-Embedder-Policy", "unsafe-none");

  // Additional security headers for production-ready app
  response.headers.set("X-Frame-Options", "SAMEORIGIN");

  response.headers.set("X-Content-Type-Options", "nosniff");

  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");

  return response;
};
