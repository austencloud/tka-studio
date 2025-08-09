import "clsx";
function useContainer(container) {
  let state = { ...container.state };
  return state;
}
export {
  useContainer as u
};
