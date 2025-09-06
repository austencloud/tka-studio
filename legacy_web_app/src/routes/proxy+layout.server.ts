// This is a placeholder proxy layout server file
// It's needed because SvelteKit is looking for this file due to the auth route structure

import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
  // This is an empty load function that doesn't do anything
  // But it satisfies SvelteKit's requirement for this file
  return {};
};
