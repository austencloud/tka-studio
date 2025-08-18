import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Arrow Mirroring Test",
    description: "Test route for arrow positioning and mirroring validation",
  };
};
