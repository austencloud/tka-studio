# Structured Logging System

This document describes the professional-grade structured logging system implemented for the Kinetic Constructor Web application.

## Overview

The logging system provides a unified approach to logging across the application, replacing the previous fragmented logging mechanisms. It offers rich contextual information, configurable output destinations, and domain-specific logging capabilities.

## Key Features

- **Unified API**: Single source of truth for all logging in the application
- **Multiple Log Levels**: TRACE, DEBUG, INFO, WARN, ERROR, FATAL
- **Structured Data**: All logs include timestamps, correlation IDs, and source information
- **Context Management**: Hierarchical context system with automatic and manual context enrichment
- **Multiple Output Destinations**: Console, memory buffer, localStorage
- **Domain-Specific Logging**: Special methods for TKA-specific domains (pictograph, sequence, motion, etc.)
- **Performance Tracking**: Built-in timing and performance monitoring
- **Error Handling**: Enhanced error logging with categorization and recovery suggestions
- **Configuration**: Runtime-configurable via URL parameters
- **Debug Panel Integration**: Visual log viewer with filtering and search

## Usage

### Basic Logging

```typescript
import { logger } from "$lib/core/logging";

// Basic logging with different levels
logger.trace("Detailed tracing information");
logger.debug("Debug information");
logger.info("General information");
logger.warn("Warning message");
logger.error("Error message");
logger.fatal("Critical error message");

// Logging with additional data
logger.info("User action", {
  data: {
    userId: "user123",
    action: "click",
    target: "button",
  },
});

// Logging errors
try {
  // Some code that might throw
} catch (error) {
  logger.error("Operation failed", { error });
}
```

### Context Management

```typescript
import { logger, createPictographContext } from "$lib/core/logging";

// Create a logger with pictograph-specific context
const pictographLogger = logger.withContext(
  createPictographContext({
    letter: "A",
    gridMode: "diamond",
  }),
);

// All logs from this logger will include the pictograph context
pictographLogger.info("Pictograph rendering started");
```

### Performance Tracking

```typescript
import { logger } from "$lib/core/logging";

// Start timing an operation
const timer = logger.startTimer("render-pictograph");

// Add checkpoints during the operation
timer.checkpoint("grid-loaded");
timer.checkpoint("props-positioned");

// End timing and log the result
timer.end({ result: "success" });
```

### Domain-Specific Logging

```typescript
import { logger } from "$lib/core/logging";

// Pictograph-specific logging
logger.pictograph("Pictograph rendering complete", {
  letter: "A",
  gridMode: "diamond",
  renderMetrics: {
    renderTime: 42,
    componentsLoaded: 5,
    totalComponents: 5,
  },
});

// SVG error logging
logger.svgError("Failed to load SVG", {
  path: "/images/props/ball.svg",
  component: "Prop",
  fallbackApplied: true,
  error: new Error("404 Not Found"),
});

// State machine transition logging
logger.transition({
  machine: "appMachine",
  from: "idle",
  to: "active",
  event: "ACTIVATE",
  duration: 15,
});
```

### URL Configuration

The logging system can be configured via URL parameters:

- `?log=debug` - Set global log level to DEBUG
- `?log=app=debug,sequence=error` - Set domain-specific log levels
- `?log=debug:console,memory` - Set log level with specific transports

## Integration with Components

### Using LoggingProvider

```svelte
<script>
  import { LoggingProvider } from '$lib/components/logging/LoggingProvider.svelte';
</script>

<LoggingProvider name="MyApp">
  <!-- Your app components -->
</LoggingProvider>
```

### Using the LogViewer

```svelte
<script>
  import { LogViewer } from '$lib/components/logging/LogViewer.svelte';
</script>

<LogViewer
  maxHeight="400px"
  showToolbar={true}
  showTimestamps={true}
  showSource={true}
  showDomain={true}
  autoScroll={true}
  initialLevel={LogLevel.INFO}
/>
```

## Integration with XState

```typescript
import { createMachine } from "xstate";
import { withLogging } from "$lib/core/logging";

// Create a machine with logging
const machine = withLogging(
  createMachine({
    // Machine configuration
  }),
  {
    name: "AppMachine",
    level: LogLevel.INFO,
    includedEvents: ["IMPORTANT_EVENT"],
    excludedEvents: ["TICK"],
    contextFields: ["userId", "currentView"],
    includeSnapshots: true,
    logTransitions: true,
    performanceTracking: {
      enabled: true,
      transitionThreshold: 50, // ms
    },
  },
);
```

## Error Handling

```typescript
import { errorLogger, ErrorCategory, ErrorSeverity } from "$lib/core/logging";

try {
  // Some code that might throw
} catch (error) {
  errorLogger.log({
    source: "MyComponent",
    message: error.message,
    stack: error.stack,
    severity: ErrorSeverity.ERROR,
    category: ErrorCategory.COMPONENT_INITIALIZATION,
    context: {
      componentProps: {
        /* relevant props */
      },
    },
  });
}
```

## Architecture

The logging system consists of the following components:

1. **Core Logger**: The main logger implementation that handles log processing and dispatching
2. **Context Management**: Utilities for managing and enriching log context
3. **Transports**: Output destinations for logs (console, memory, localStorage)
4. **Configuration**: System for configuring logging behavior
5. **Machine Logger**: Integration with XState for state machine logging
6. **Error Logger**: Enhanced error logging with categorization and recovery suggestions
7. **Component Integration**: Svelte components for logging context and visualization

## Extending the System

### Adding a New Transport

```typescript
import { type LogTransport, type LogEntry } from "$lib/core/logging";

export class MyCustomTransport implements LogTransport {
  name = "custom";

  log(entry: LogEntry): void {
    // Custom log handling logic
  }

  // Optional methods
  flush?(): Promise<void> {
    // Flush logs to destination
  }

  clear?(): void {
    // Clear stored logs
  }

  getEntries?(): LogEntry[] {
    // Return stored logs
  }
}

// Register the transport
logger.setConfig({
  transports: [new MyCustomTransport()],
});
```

### Adding a New Domain-Specific Logger

```typescript
// Extend the Logger interface
declare module "$lib/core/logging" {
  interface Logger {
    myDomain(message: string, params: MyDomainParams): void;
  }

  interface MyDomainParams {
    // Domain-specific parameters
  }
}

// Implement the method in LoggerImpl
LoggerImpl.prototype.myDomain = function (
  message: string,
  params: MyDomainParams,
): void {
  this.log(LogLevel.INFO, message, {
    domain: LogDomain.MY_DOMAIN,
    data: params,
  });
};
```

## Best Practices

1. **Use Appropriate Log Levels**:

   - TRACE: Extremely detailed information for debugging complex issues
   - DEBUG: Detailed information useful during development
   - INFO: General information about application flow
   - WARN: Potential issues that aren't errors
   - ERROR: Error conditions that might allow recovery
   - FATAL: Severe errors that prevent normal operation

2. **Include Contextual Information**:

   - Always provide relevant context with logs
   - Use domain-specific logging methods when appropriate
   - Include correlation IDs for related operations

3. **Performance Considerations**:

   - Use sampling for high-volume logs in production
   - Be mindful of the performance impact of logging
   - Consider using the memory transport only in development

4. **Error Logging**:

   - Always include the original error object when logging errors
   - Categorize errors appropriately
   - Include recovery suggestions when possible

5. **Configuration**:
   - Set appropriate default log levels for different environments
   - Use URL parameters for debugging specific issues
   - Consider disabling verbose logging in production
