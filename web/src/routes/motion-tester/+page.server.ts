import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  return {
    meta: {
      title: "Animator - TKA Development | Flow Arts Animation Testing",
      description:
        "Development tool for testing motion parameters and animation sequences in TKA. Debug flow arts movements and kinetic patterns.",
      canonical: "https://thekineticalphabet.com/motion-tester",
      ogTitle: "Animator - TKA Development",
      ogDescription:
        "Test and debug motion parameters for flow arts animations with TKA's motion testing interface.",
      ogType: "website",
      ogUrl: "https://thekineticalphabet.com/motion-tester",
    },
  };
};
