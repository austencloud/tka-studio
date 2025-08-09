const load = async ({ params, url }) => {
  return {
    platform: params.platform,
    code: url.searchParams.get("code"),
    state: url.searchParams.get("state")
  };
};
export {
  load
};
