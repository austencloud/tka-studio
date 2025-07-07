<!--
  Logging System Test Component
  
  This component demonstrates the various features of the logging system.
-->
<script lang="ts">
  import { onMount } from 'svelte';
  import { 
    logger, 
    LogLevel, 
    LogDomain,
    createPictographContext,
    createSequenceContext,
    createSvgContext,
    createStateContext,
    errorLogger,
    ErrorSeverity,
    ErrorCategory
  } from '../../logging';
	// import LogViewer from '../components/logging/LogViewer.svelte'; // TODO: Create LogViewer component
  
  // Test basic logging
  function testBasicLogging() {
    logger.trace('This is a trace message');
    logger.debug('This is a debug message');
    logger.info('This is an info message');
    logger.warn('This is a warning message');
    logger.error('This is an error message');
    logger.fatal('This is a fatal message');
    
    logger.info('Message with data', {
      data: {
        userId: 'user123',
        action: 'click',
        target: 'button'
      }
    });
  }
  
  // Test context management
  function testContextManagement() {
    // Create a logger with pictograph context
    const pictographLogger = logger.withContext(createPictographContext({
      letter: 'A',
      gridMode: 'diamond'
    }));
    
    pictographLogger.info('Pictograph rendering started');
    
    // Create a logger with sequence context
    const sequenceLogger = logger.withContext(createSequenceContext({
      sequenceId: 'seq123',
      motionType: 'pro',
      gridType: 'diamond'
    }));
    
    sequenceLogger.info('Sequence creation started');
    
    // Create a logger with SVG context
    const svgLogger = logger.withContext(createSvgContext({
      path: '/images/props/ball.svg',
      component: 'Prop'
    }));
    
    svgLogger.info('SVG loading started');
    
    // Create a logger with state context
    const stateLogger = logger.withContext(createStateContext({
      machine: 'appMachine',
      state: 'idle'
    }));
    
    stateLogger.info('State machine initialized');
  }
  
  // Test performance tracking
  function testPerformanceTracking() {
    const timer = logger.startTimer('test-operation');
    
    setTimeout(() => {
      timer.checkpoint('checkpoint-1');
      
      setTimeout(() => {
        timer.checkpoint('checkpoint-2');
        
        setTimeout(() => {
          timer.end({ result: 'success' });
        }, 50);
      }, 30);
    }, 20);
  }
  
  // Test domain-specific logging
  function testDomainSpecificLogging() {
    // Pictograph logging
    logger.pictograph('Pictograph rendering complete', {
      letter: 'A',
      gridMode: 'diamond',
      componentState: 'complete',
      renderMetrics: {
        renderTime: 42,
        componentsLoaded: 5,
        totalComponents: 5
      }
    });
    
    // SVG error logging
    logger.svgError('Failed to load SVG', {
      path: '/images/props/ball.svg',
      component: 'Prop',
      fallbackApplied: true,
      error: new Error('404 Not Found')
    });
    
    // State machine transition logging
    logger.transition({
      machine: 'appMachine',
      from: 'idle',
      to: 'active',
      event: 'ACTIVATE',
      duration: 15
    });
  }
  
  // Test error logging
  function testErrorLogging() {
    try {
      throw new Error('Test error');
    } catch (error) {
      errorLogger.log({
        source: 'LoggingTest',
        message: 'Test error occurred',
        stack: error instanceof Error ? error.stack : undefined,
        severity: ErrorSeverity.ERROR,
        category: ErrorCategory.COMPONENT_INITIALIZATION,
        context: {
          testId: 'test123'
        }
      });
    }
  }
  
  // Run all tests
  function runAllTests() {
    logger.info('Starting logging system tests', {
      data: {
        testTime: new Date().toISOString()
      }
    });
    
    testBasicLogging();
    testContextManagement();
    testPerformanceTracking();
    testDomainSpecificLogging();
    testErrorLogging();
    
    logger.info('All logging system tests completed');
  }
  
  onMount(() => {
    // Don't run tests automatically to avoid cluttering the logs
  });
</script>

<div class="logging-test">
  <h1>Logging System Test</h1>
  
  <div class="test-controls">
    <button on:click={runAllTests}>Run All Tests</button>
    <button on:click={testBasicLogging}>Test Basic Logging</button>
    <button on:click={testContextManagement}>Test Context Management</button>
    <button on:click={testPerformanceTracking}>Test Performance Tracking</button>
    <button on:click={testDomainSpecificLogging}>Test Domain-Specific Logging</button>
    <button on:click={testErrorLogging}>Test Error Logging</button>
  </div>
  
  <div class="log-viewer-container">
    <h2>Log Viewer</h2>
    <LogViewer 
      maxHeight="400px"
      showToolbar={true}
      showTimestamps={true}
      showSource={true}
      showDomain={true}
      autoScroll={true}
      initialLevel={LogLevel.DEBUG}
    />
  </div>
</div>

<style>
  .logging-test {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  h1, h2 {
    color: #333;
  }
  
  .test-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  button {
    padding: 8px 16px;
    background-color: #4299e1;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
  
  button:hover {
    background-color: #3182ce;
  }
  
  .log-viewer-container {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    background-color: #f8fafc;
  }
</style>
