/**
 * Logging Configuration System
 *
 * Handles parsing and applying logging configuration from various sources.
 */

import { browser } from '$app/environment';
import {
  LogLevel,
  LOG_LEVEL_MAP,
  type LoggerConfig,
  LogDomain
} from './types';
import {
  DEFAULT_LOGGER_CONFIG,
  LOG_URL_PARAM
} from './constants';
import { ConsoleTransport } from './transports/console';
import { MemoryTransport } from './transports/memory';
import { LocalStorageTransport } from './transports/localStorage';

/**
 * Parse log configuration from URL parameters
 *
 * Supports formats like:
 * - ?log=debug (global level)
 * - ?log=app=debug,sequence=error (domain-specific levels)
 * - ?log=debug:console,memory (level with transports)
 * - ?log=app=debug:console,pictograph=info:memory (domain-specific with transports)
 */
export function parseLogConfig(): Partial<LoggerConfig> | null {
  if (!browser) return null;

  const url = new URL(window.location.href);
  const logParam = url.searchParams.get(LOG_URL_PARAM);

  if (!logParam) return null;

  const config: Partial<LoggerConfig> = {
    transports: []
  };

  // Check if it's a simple global level like "debug"
  if (logParam in LOG_LEVEL_MAP) {
    config.minLevel = LOG_LEVEL_MAP[logParam as keyof typeof LOG_LEVEL_MAP];
    config.transports = createDefaultTransports();
    return config;
  }

  // Parse more complex configurations
  const enabledDomains: LogDomain[] = [];
  const disabledDomains: LogDomain[] = [];

  logParam.split(',').forEach(part => {
    // Check for domain=level:transports format
    if (part.includes('=')) {
      const [domain, levelAndTransports] = part.split('=');

      // Parse level and transports
      let level: string;
      let transports: string[] = [];

      if (levelAndTransports.includes(':')) {
        [level, ...transports] = levelAndTransports.split(':');
      } else {
        level = levelAndTransports;
      }

      // Handle domain-specific configuration
      if (domain && level) {
        // Check if it's a negation (e.g., !app=debug)
        const isDomainDisabled = domain.startsWith('!');
        const domainName = isDomainDisabled ? domain.substring(1) : domain;

        // Check if it's a valid domain
        if (Object.values(LogDomain).includes(domainName as LogDomain)) {
          if (isDomainDisabled) {
            disabledDomains.push(domainName as LogDomain);
          } else {
            enabledDomains.push(domainName as LogDomain);
          }
        }

        // Set global level if domain is 'all'
        if (domainName === 'all' && level in LOG_LEVEL_MAP) {
          config.minLevel = LOG_LEVEL_MAP[level as keyof typeof LOG_LEVEL_MAP];
        }
      }
    }
    // Check for level:transports format
    else if (part.includes(':')) {
      const [level, ...transports] = part.split(':');

      if (level in LOG_LEVEL_MAP) {
        config.minLevel = LOG_LEVEL_MAP[level as keyof typeof LOG_LEVEL_MAP];
      }
    }
    // Simple level
    else if (part in LOG_LEVEL_MAP) {
      config.minLevel = LOG_LEVEL_MAP[part as keyof typeof LOG_LEVEL_MAP];
    }
  });

  // Set enabled/disabled domains
  if (enabledDomains.length > 0) {
    config.enabledDomains = enabledDomains;
  }

  if (disabledDomains.length > 0) {
    config.disabledDomains = disabledDomains;
  }

  // Create default transports if none specified
  if (!config.transports || config.transports.length === 0) {
    config.transports = createDefaultTransports();
  }

  return config;
}

/**
 * Create default transports based on environment
 */
export function createDefaultTransports(): ConsoleTransport[] {
  return [
    new ConsoleTransport({
      prettyPrint: import.meta.env.DEV,
      includeTimestamps: true,
      includeSource: true,
      includeDomain: true,
      includeCorrelationId: true
    })
  ];
}

/**
 * Create development transports (console + memory)
 */
export function createDevTransports(): (ConsoleTransport | MemoryTransport)[] {
  return [
    new ConsoleTransport({
      prettyPrint: true,
      includeTimestamps: true,
      includeSource: true,
      includeDomain: true,
      includeCorrelationId: true
    }),
    new MemoryTransport({
      maxEntries: 1000,
      circular: true
    })
  ];
}

/**
 * Create production transports (console + localStorage)
 */
export function createProdTransports(): (ConsoleTransport | LocalStorageTransport)[] {
  return [
    new ConsoleTransport({
      prettyPrint: false,
      includeTimestamps: true,
      includeSource: true,
      includeDomain: false,
      includeCorrelationId: false
    }),
    new LocalStorageTransport({
      maxEntries: 500,
      minLevel: LogLevel.ERROR,
      throttleMs: 5000
    })
  ];
}

/**
 * Create a full configuration object with appropriate defaults
 */
export function createLoggerConfig(config: Partial<LoggerConfig> = {}): LoggerConfig {
  const baseConfig = { ...DEFAULT_LOGGER_CONFIG };

  // Set environment-appropriate transports if none provided
  if (!config.transports || config.transports.length === 0) {
    baseConfig.transports = import.meta.env.DEV
      ? createDevTransports()
      : createProdTransports();
  }

  return {
    ...baseConfig,
    ...config,
    // Merge arrays instead of replacing
    transports: [...(baseConfig.transports || []), ...(config.transports || [])]
  };
}
