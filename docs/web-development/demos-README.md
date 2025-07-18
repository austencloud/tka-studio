# TKA Application Factory Demonstrations

This directory contains comprehensive demonstrations of the TKA Application Factory implementation, showcasing how different application modes work in practice with visual verification and real-world scenarios.

## 🎯 Overview

The Application Factory enables TKA to run in different modes:
- **TEST**: Fast in-memory testing with mock services (perfect for AI agents)
- **HEADLESS**: Real business logic without UI components (ideal for server-side processing)
- **PRODUCTION**: Full desktop application with real services
- **RECORDING**: Production services with recording capability (future feature)

## 📁 Demonstration Scripts

### 1. `application_factory_interactive_demo.py`
**Interactive Mode Demonstration**

Shows how each application mode works with side-by-side comparisons.

```bash
python application_factory_interactive_demo.py
```

**What it demonstrates:**
- Container creation for each mode
- Service resolution and usage
- Performance differences between modes
- Memory usage and execution time comparisons
- Service behavior differences (mock vs real)

**Key Output:**
- Service registration counts per mode
- Execution time comparisons
- Memory usage deltas
- Side-by-side operation results

### 2. `tka_workflow_scenarios.py`
**TKA Workflow Scenarios**

Demonstrates realistic TKA workflows across different application modes.

```bash
python tka_workflow_scenarios.py
```

**What it demonstrates:**
- Sequence creation and management workflows
- Layout calculation scenarios
- Settings management operations
- Cross-mode performance comparisons
- Real-world TKA usage patterns

**Key Output:**
- Workflow execution summaries
- Performance metrics per workflow
- Success/failure rates
- Mode-specific behavior differences

### 3. `ai_agent_integration_examples.py`
**AI Agent Integration Examples**

Shows how AI agents can use the factory for automated testing and batch processing.

```bash
python ai_agent_integration_examples.py
```

**What it demonstrates:**
- Automated test suite execution
- Batch sequence processing
- Error handling and recovery
- Test report generation
- Integration patterns for external tools

**Key Output:**
- Automated test results with success rates
- Batch processing performance metrics
- Comprehensive test reports in JSON format
- Error handling examples

### 4. `performance_comparison_demo.py`
**Performance Comparison Analysis**

Provides detailed performance metrics and comparisons between modes.

```bash
python performance_comparison_demo.py
```

**What it demonstrates:**
- Container creation performance
- Operation execution benchmarks
- Memory usage analysis
- CPU utilization comparisons
- Scalability testing

**Key Output:**
- Detailed performance metrics
- Cross-mode comparison tables
- Memory usage graphs (text-based)
- Performance recommendations

### 5. `run_all_demos.py`
**Complete Demonstration Suite**

Runs all demonstration scripts with comprehensive reporting.

```bash
python run_all_demos.py
```

**What it demonstrates:**
- Complete Application Factory capabilities
- End-to-end verification
- Comprehensive reporting
- Usage recommendations

**Key Output:**
- Summary of all demonstrations
- Success/failure rates
- Total execution time
- Key insights and recommendations

## 🚀 Quick Start

### Run All Demonstrations
```bash
cd demos
python run_all_demos.py
```

### Run Individual Demonstrations
```bash
# Interactive demo with mode comparisons
python application_factory_interactive_demo.py

# Realistic workflow scenarios
python tka_workflow_scenarios.py

# AI agent integration examples
python ai_agent_integration_examples.py

# Performance analysis
python performance_comparison_demo.py
```

## 📊 Expected Output Examples

### Container Creation Comparison
```
🏗️ Benchmarking Container Creation
----------------------------------------
✅ test         | 0.0234s | +2.45MB | CPU: 15.2%
✅ headless     | 0.0456s | +4.12MB | CPU: 18.7%
✅ production   | 0.1234s | +8.93MB | CPU: 25.4%
```

### Service Operation Results
```
🎵 Sequence Operations Comparison
test        | Create: 0.000123s | Save: 0.000045s | ID: seq_0
headless    | Create: 0.001234s | Save: 0.000234s | ID: seq_0
production  | Create: 0.005678s | Save: 0.002345s | ID: uuid-string
```

### AI Agent Test Results
```
📋 TEST EXECUTION REPORT
========================================
Mode: test
Total Tests: 15
Passed: 14
Failed: 1
Success Rate: 93.3%
Total Duration: 2.3456s
Average Duration: 0.1564s
```

## 🎯 Use Cases Demonstrated

### For AI Agents
- **Automated Testing**: Run comprehensive test suites without UI dependencies
- **Batch Processing**: Process multiple sequences in headless mode
- **Integration Testing**: Verify TKA functionality programmatically
- **Performance Testing**: Benchmark operations across modes

### For Developers
- **Mode Selection**: Choose appropriate mode for specific use cases
- **Performance Analysis**: Compare execution times and memory usage
- **Service Verification**: Ensure services work correctly in all modes
- **Integration Patterns**: Learn how to integrate with TKA programmatically

### For System Administrators
- **Server Deployment**: Use headless mode for server-side TKA processing
- **CI/CD Integration**: Run tests in automated pipelines
- **Performance Monitoring**: Track TKA performance across environments
- **Resource Planning**: Understand memory and CPU requirements

## 🔧 Technical Details

### Dependencies
- TKA Application Factory implementation
- Python 3.9+
- psutil (for performance monitoring)
- Standard library modules (time, json, subprocess, etc.)

### Performance Characteristics
- **TEST mode**: Fastest execution, lowest memory usage, predictable results
- **HEADLESS mode**: Moderate performance, real business logic, no UI overhead
- **PRODUCTION mode**: Full functionality, highest resource usage, complete features

### Error Handling
All demonstrations include comprehensive error handling:
- Graceful degradation when modes are unavailable
- Detailed error reporting with stack traces
- Timeout protection for long-running operations
- Recovery strategies for common failure scenarios

## 📈 Performance Insights

Based on the demonstrations, you can expect:

### Execution Speed (relative)
- TEST mode: 1x (baseline - fastest)
- HEADLESS mode: 2-5x slower than test
- PRODUCTION mode: 5-20x slower than test

### Memory Usage (relative)
- TEST mode: 1x (baseline - lowest)
- HEADLESS mode: 1.5-3x more than test
- PRODUCTION mode: 3-10x more than test

### Use Case Recommendations
- **Rapid prototyping**: TEST mode
- **Automated testing**: TEST mode
- **Server-side processing**: HEADLESS mode
- **Batch operations**: HEADLESS mode
- **Full application**: PRODUCTION mode
- **User interaction**: PRODUCTION mode

## 🎉 Success Criteria

After running the demonstrations, you should see:
- ✅ All application modes create containers successfully
- ✅ Services resolve and execute operations correctly
- ✅ Performance differences are clearly visible
- ✅ Mock services provide predictable, fast results
- ✅ Real services provide complete functionality
- ✅ Error handling works gracefully
- ✅ AI agent integration patterns are clear

## 🔍 Troubleshooting

### Common Issues
1. **Import Errors**: Ensure TKA src path is correctly added to sys.path
2. **Missing Dependencies**: Install required packages (psutil, etc.)
3. **Permission Errors**: Run with appropriate file system permissions
4. **Memory Issues**: Close other applications if running performance tests

### Debug Mode
Add `--debug` flag to any script for verbose output:
```bash
python application_factory_interactive_demo.py --debug
```

## 📝 Next Steps

After reviewing the demonstrations:
1. Choose the appropriate mode for your use case
2. Integrate the Application Factory into your workflows
3. Use TEST mode for rapid development and testing
4. Deploy HEADLESS mode for production server environments
5. Leverage the performance insights for optimization

The Application Factory eliminates the complexity of TKA application setup and enables seamless switching between different operational modes based on your specific requirements.
