// src/routes/auth/callback/[platform]/+page.server.ts
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, url }) => {
  // Just pass the parameters to the client component
  // In a real implementation, you might handle token exchange on the server
  return {
    platform: params.platform,
    code: url.searchParams.get("code"),
    state: url.searchParams.get("state"),
  };
};
