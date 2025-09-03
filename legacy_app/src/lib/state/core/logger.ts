/**
 * State Machine Logger
 *
 * Configurable logging for state machines to control verbosity
 */

import { browser } from '$app/environment';

export enum LogLevel {
  NONE = 0,
  ERROR = 1,
  WARN = 2,
  INFO = 3,
  DEBUG = 4
}

// Default log level based on environment
const DEFAULT_LOG_LEVEL = import.meta.env.DEV ? LogLevel.ERROR : LogLevel.NONE;

// Global log level setting
let globalLogLevel = DEFAULT_LOG_LEVEL;

// Map of machine IDs to their specific log levels
const machineLogLevels = new Map<string, LogLevel>();

/**
 * Configure the global log level for all state machines
 */
export function setGlobalLogLevel(level: LogLevel): void {
  globalLogLevel = level;
}

/**
 * Configure a specific log level for a particular machine
 */
export function setMachineLogLevel(machineId: string, level: LogLevel): void {
  machineLogLevels.set(machineId, level);
}

/**
 * Get the effective log level for a machine
 */
export function getLogLevel(machineId: string): LogLevel {
  return machineLogLevels.get(machineId) ?? globalLogLevel;
}

/**
 * Check if a particular log level should be shown for a machine
 */
export function shouldLog(machineId: string, level: LogLevel): boolean {
  const effectiveLevel = getLogLevel(machineId);
  return level <= effectiveLevel;
}

/**
 * Log a message if the level is appropriate
 */
export function log(machineId: string, level: LogLevel, ...args: any[]): void {
  if (!shouldLog(machineId, level)) return;

  switch (level) {
    case LogLevel.ERROR:
      console.error(`[${machineId}]`, ...args);
      break;
    case LogLevel.WARN:
      console.warn(`[${machineId}]`, ...args);
      break;
    case LogLevel.INFO:
      console.info(`[${machineId}]`, ...args);
      break;
    case LogLevel.DEBUG:
      console.debug(`[${machineId}]`, ...args);
      break;
  }
}

// Initialize from URL parameters if in browser
if (browser) {
  const url = new URL(window.location.href);
  const logParam = url.searchParams.get('log');

  if (logParam) {
    // Parse log level from URL
    const levelMap: Record<string, LogLevel> = {
      'none': LogLevel.NONE,
      'error': LogLevel.ERROR,
      'warn': LogLevel.WARN,
      'info': LogLevel.INFO,
      'debug': LogLevel.DEBUG
    };

    // Check for machine-specific settings like "app=debug,sequence=error"
    if (logParam.includes('=')) {
      logParam.split(',').forEach(part => {
        const [machineId, levelName] = part.split('=');
        if (machineId && levelName && levelName in levelMap) {
          setMachineLogLevel(machineId, levelMap[levelName]);
        }
      });
    }
    // Or a global setting like "debug"
    else if (logParam in levelMap) {
      setGlobalLogLevel(levelMap[logParam]);
    }
  }
}
