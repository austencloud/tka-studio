/**
 * Safe JSCodeshift transform - ONLY replaces $domain with $shared/domain
 * Does nothing else to avoid breaking anything
 */

module.exports = function transformer(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  let hasChanges = false;

  // ONLY replace $domain imports with $shared/domain
  // This is the safest possible change
  root.find(j.ImportDeclaration).forEach((path) => {
    const importSource = path.value.source.value;

    if (importSource === "$domain") {
      path.value.source.value = "$shared/domain";
      hasChanges = true;
      console.log(`${fileInfo.path}: $domain -> $shared/domain`);
    }
  });

  return hasChanges ? root.toSource({ quote: "single" }) : null;
};

module.exports.parser = "ts";
