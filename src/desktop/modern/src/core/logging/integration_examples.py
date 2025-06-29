"""
Integration examples for upgrading existing services to use smart logging.

This file shows how to retrofit the arrow positioning services that were
generating verbose logs with the new smart logging system.
"""

# Example 1: Upgrading ArrowAdjustmentCalculatorService

from core.logging import get_arrow_positioning_logger, log_arrow_adjustment


class ArrowAdjustmentCalculatorServiceUpgraded:
    """
    Upgraded version of ArrowAdjustmentCalculatorService using smart logging.
    
    CHANGES MADE:
    1. Replace direct logger calls with smart logger
    2. Use batch letter-based logging instead of individual calculations
    3. Add performance-based verbosity
    4. Suppress repetitive logs
    """
    
    def __init__(self, lookup_service=None, tuple_processor=None):
        # Get the specialized arrow positioning logger
        self.arrow_logger = get_arrow_positioning_logger()
        
        # Initialize services as before
        self.lookup_service = lookup_service or self._create_default_lookup_service()
        self.tuple_processor = tuple_processor or self._create_default_tuple_processor()
    
    @log_arrow_adjustment  # This decorator handles performance-based logging
    def calculate_adjustment_result(self, arrow_data, pictograph_data):
        """
        Calculate arrow position adjustment with smart logging.
        
        BEFORE: Generated 6+ log lines per calculation
        AFTER: Batched summary per letter, details only if slow/error
        """
        letter = pictograph_data.letter
        
        # Start tracking this letter's operations
        self.arrow_logger.start_letter_positioning(letter)
        
        motion = arrow_data.motion_data
        if not motion:
            # Error handling - still logged in detail
            error_msg = "No motion data available for adjustment calculation"
            self.arrow_logger.letter_operations[letter]['errors'].append(error_msg)
            return failure(app_error(ErrorType.VALIDATION_ERROR, error_msg))
        
        try:
            # STEP 1: Base adjustment lookup (now silent unless slow)
            lookup_result = self.lookup_service.get_base_adjustment(arrow_data, pictograph_data)
            if lookup_result.is_failure():
                self.arrow_logger.letter_operations[letter]['errors'].append(str(lookup_result.error))
                return failure(lookup_result.error)
            
            base_adjustment = lookup_result.value
            
            # OLD CODE - removed verbose logging:
            # logger.info(f"🎯 Calculating adjustment for {arrow_data.color} arrow in letter {letter}")
            # logger.info(f"   Step 1 - Base adjustment: ({base_adjustment.x:.1f}, {base_adjustment.y:.1f})")
            
            # STEP 2: Process directional tuples (now with smart logging)
            tuple_result = self.tuple_processor.process_directional_tuples(
                base_adjustment, arrow_data, pictograph_data
            )
            if tuple_result.is_failure():
                self.arrow_logger.letter_operations[letter]['errors'].append(str(tuple_result.error))
                return failure(tuple_result.error)
            
            final_adjustment = tuple_result.value
            
            # OLD CODE - removed verbose logging:
            # logger.info(f"   Final adjustment: ({final_adjustment.x:.1f}, {final_adjustment.y:.1f})")
            
            # Finish tracking and log summary
            self.arrow_logger.finish_letter_positioning(letter)
            
            return success(final_adjustment)
            
        except Exception as e:
            self.arrow_logger.letter_operations[letter]['errors'].append(str(e))
            self.arrow_logger.finish_letter_positioning(letter)
            return failure(app_error(ErrorType.POSITIONING_ERROR, f"Unexpected error: {e}", {}, e))


# Example 2: Upgrading DirectionalTupleProcessor

from core.logging import log_directional_processing


class DirectionalTupleProcessorUpgraded:
    """
    Upgraded DirectionalTupleProcessor with smart logging.
    
    CHANGES MADE:
    1. Suppress "Generated directional tuples" logs unless slow
    2. Suppress "Quadrant index" logs unless slow  
    3. Suppress "Final adjustment" logs unless slow
    4. Use letter-based batching
    """
    
    def __init__(self, directional_tuple_service, quadrant_index_service):
        self.directional_tuple_service = directional_tuple_service
        self.quadrant_index_service = quadrant_index_service
        self.arrow_logger = get_arrow_positioning_logger()
    
    @log_directional_processing  # Handles performance-based logging automatically
    def process_directional_tuples(self, base_adjustment, arrow_data, pictograph_data):
        """
        Process directional tuples with minimal logging.
        
        BEFORE: 3+ log lines per processing call
        AFTER: Silent unless slow (>20ms) or error
        """
        motion = arrow_data.motion_data
        if not motion:
            return failure(app_error(ErrorType.VALIDATION_ERROR, "No motion data"))
        
        try:
            # STEP 1: Generate tuples (now silent unless slow)
            tuples_result = self._generate_directional_tuples(motion, base_adjustment)
            if tuples_result.is_failure():
                return failure(tuples_result.error)
            
            directional_tuples = tuples_result.value
            
            # OLD CODE - removed verbose logging:
            # logger.info(f"Generated directional tuples: {directional_tuples}")
            
            # STEP 2: Get quadrant index (now silent unless slow)
            quadrant_result = self._get_quadrant_index(arrow_data, pictograph_data)
            if quadrant_result.is_failure():
                return failure(quadrant_result.error)
            
            quadrant_index = quadrant_result.value
            
            # OLD CODE - removed verbose logging:
            # logger.info(f"Quadrant index: {quadrant_index}")
            
            # STEP 3: Select final adjustment (now silent unless slow)
            selection_result = self._select_from_tuples(directional_tuples, quadrant_index)
            if selection_result.is_failure():
                return failure(selection_result.error)
            
            final_adjustment = selection_result.value
            
            # OLD CODE - removed verbose logging:
            # logger.info(f"Final adjustment: ({final_adjustment.x:.1f}, {final_adjustment.y:.1f})")
            
            # The @log_directional_processing decorator automatically logs performance
            # Only if this operation takes >20ms will it be logged
            
            return success(final_adjustment)
            
        except Exception as e:
            # Errors are still logged in detail by the decorator
            return failure(app_error(ErrorType.POSITIONING_ERROR, f"Error: {e}", {}, e))


# Example 3: Upgrading ArrowAdjustmentLookupService

from core.logging import log_adjustment_lookup


class ArrowAdjustmentLookupServiceUpgraded:
    """
    Upgraded lookup service with suppressed verbose logs.
    
    CHANGES MADE:
    1. Suppress "Using special placement" logs
    2. Suppress "Using default calculation" logs  
    3. Track lookups for letter-based summary
    """
    
    def __init__(self, special_placement_service, default_placement_service, **kwargs):
        self.special_placement_service = special_placement_service
        self.default_placement_service = default_placement_service
        self.arrow_logger = get_arrow_positioning_logger()
    
    @log_adjustment_lookup  # Performance-based logging
    def get_base_adjustment(self, arrow_data, pictograph_data):
        """
        Get base adjustment with minimal logging.
        
        BEFORE: "Using special placement" or "Using default calculation" every call
        AFTER: Silent success, errors only when they occur
        """
        try:
            # Try special placement first
            special_result = self._try_special_placement(arrow_data, pictograph_data)
            if special_result.is_success():
                # OLD CODE - removed verbose logging:
                # logger.info(f"Using special placement: {special_result.value}")
                
                # Track for summary (letter-based batching handles logging)
                return success(special_result.value)
            
            # Fall back to default placement
            default_result = self._try_default_placement(arrow_data, pictograph_data)
            if default_result.is_success():
                # OLD CODE - removed verbose logging:
                # logger.info(f"Using default calculation: {default_result.value}")
                
                return success(default_result.value)
            
            # Both failed
            return failure(app_error(
                ErrorType.POSITIONING_ERROR,
                "Both special and default placement failed"
            ))
            
        except Exception as e:
            # Errors are still logged by the decorator
            return failure(app_error(ErrorType.POSITIONING_ERROR, f"Lookup error: {e}", {}, e))


# Example 4: Integration with ApplicationFactory

def upgrade_application_factory():
    """
    Example of how to integrate smart logging with your ApplicationFactory.
    """
    from core.application.application_factory import ApplicationFactory
    from core.logging import setup_smart_logging, setup_arrow_positioning_logging_only
    
    class ApplicationFactoryWithSmartLogging(ApplicationFactory):
        """Extended ApplicationFactory with smart logging integration."""
        
        @staticmethod
        def create_production_app():
            """Production app with minimal logging."""
            # Configure quiet logging first
            setup_arrow_positioning_logging_only(quiet=True)
            
            # Create container as before
            container = ApplicationFactory.create_production_app()
            return container
        
        @staticmethod  
        def create_test_app():
            """Test app with test-optimized logging."""
            # Configure test logging (very quiet)
            setup_smart_logging('testing')
            
            container = ApplicationFactory.create_test_app()
            return container
        
        @staticmethod
        def create_headless_app():
            """Headless app with performance monitoring."""
            # Configure development logging with performance tracking
            setup_smart_logging('development')
            
            container = ApplicationFactory.create_headless_app()
            return container


# Example 5: Quick Fix for Immediate Relief

def apply_immediate_logging_fix():
    """
    Apply immediate fix to existing services without code changes.
    
    This can be called in main.py to instantly reduce verbosity.
    """
    from core.logging import setup_arrow_positioning_logging_only
    
    # Instant relief - suppress verbose arrow positioning logs
    setup_arrow_positioning_logging_only(quiet=True)
    
    print("🔇 Arrow positioning verbosity REDUCED")
    print("   - Directional tuple logs: SUPPRESSED")
    print("   - Quadrant index logs: SUPPRESSED") 
    print("   - Adjustment calculation logs: SUPPRESSED")
    print("   - Summary logs: ENABLED")


# Example 6: Environment-based Configuration

def configure_logging_for_environment():
    """
    Configure logging based on environment detection.
    """
    import os
    from core.logging import setup_smart_logging, enable_quiet_mode
    
    # Check environment
    if os.getenv('TKA_ENVIRONMENT') == 'production':
        enable_quiet_mode()
        print("🔇 Production mode: Quiet logging enabled")
        
    elif os.getenv('TKA_DEBUG_POSITIONING') == 'true':
        setup_smart_logging('debug')
        print("📢 Debug mode: Verbose positioning logs enabled")
        
    else:
        # Default: reduce arrow positioning noise but keep other logs
        setup_arrow_positioning_logging_only(quiet=False)
        print("🔧 Development mode: Smart logging enabled")


# Example 7: Performance Monitoring

def enable_positioning_performance_monitoring():
    """
    Enable performance monitoring for positioning operations.
    """
    from core.logging import get_arrow_positioning_logger, enable_performance_monitoring
    
    enable_performance_monitoring()
    arrow_logger = get_arrow_positioning_logger()
    
    def log_performance_summary():
        """Log performance summary for positioning operations."""
        report = arrow_logger.get_positioning_performance_report()
        
        if report['total_letters'] > 0:
            print(f"📊 POSITIONING PERFORMANCE REPORT:")
            print(f"   Letters processed: {report['total_letters']}")
            print(f"   Arrows positioned: {report['total_arrows']}")
            print(f"   Total time: {report['total_duration_ms']:.1f}ms")
            print(f"   Avg per letter: {report['avg_time_per_letter_ms']:.1f}ms")
            print(f"   Avg per arrow: {report['avg_time_per_arrow_ms']:.1f}ms")
            print(f"   Errors: {report['total_errors']}")
    
    return log_performance_summary


if __name__ == "__main__":
    # Quick test of the integration
    print("🧪 Testing smart logging integration...")
    
    # Apply immediate fix
    apply_immediate_logging_fix()
    
    # Test environment configuration
    configure_logging_for_environment()
    
    print("✅ Smart logging integration examples ready!")
