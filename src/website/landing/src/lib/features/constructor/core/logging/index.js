// Logging utilities
export const logger = {
  debug: (message, ...args) => console.debug("[TKA-DEBUG]", message, ...args),
  info: (message, ...args) => console.info("[TKA-INFO]", message, ...args),
  warn: (message, ...args) => console.warn("[TKA-WARN]", message, ...args),
  error: (message, ...args) => console.error("[TKA-ERROR]", message, ...args),
  log: (message, ...args) => console.log("[TKA-LOG]", message, ...args),
};

// Export as default as well for compatibility
export default logger;
