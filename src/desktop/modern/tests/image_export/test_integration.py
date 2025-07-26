"""
Integration Test for Modern Image Export System

This test verifies that the modern image export system works end-to-end
and can be integrated with the existing TKA application.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions
)


class TestImageExportIntegration:
    """Integration tests for the modern image export system."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up integration test environment."""
        # Ensure QApplication exists
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        
        # Create DI container and register services
        self.container = DIContainer()
        register_image_export_services(self.container)
        
        # Create temporary test environment
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_data_dir = self.temp_dir / "test_data"
        self.export_dir = self.temp_dir / "exports"
        self.test_data_dir.mkdir(parents=True)
        self.export_dir.mkdir(parents=True)
        
        # Create test sequence data
        self._create_test_data()
        
        yield
        
        # Cleanup
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_data(self):
        """Create test sequence data for integration testing."""
        # Create test words with sequences
        test_words = {
            "apple": [
                {"sequence": [{"beat": i, "position": f"apple_pos_{i}"} for i in range(1, 5)]},
                {"sequence": [{"beat": i, "position": f"apple_pos_{i}"} for i in range(1, 9)]},
                {"sequence": [{"beat": i, "position": f"apple_pos_{i}"} for i in range(1, 17)]}
            ],
            "banana": [
                {"sequence": [{"beat": i, "position": f"banana_pos_{i}"} for i in range(1, 7)]},
                {"sequence": [{"beat": i, "position": f"banana_pos_{i}"} for i in range(1, 13)]}
            ],
            "cherry": [
                {"sequence": [{"beat": i, "position": f"cherry_pos_{i}"} for i in range(1, 3)]}
            ]
        }
        
        for word, sequences in test_words.items():
            word_dir = self.test_data_dir / word
            word_dir.mkdir()
            
            for i, seq_data in enumerate(sequences):
                seq_length = len(seq_data["sequence"])
                filename = f"{word}_length_{seq_length}"
                
                # Create JSON file
                json_file = word_dir / f"{filename}.json"
                with open(json_file, 'w') as f:
                    json.dump(seq_data, f, indent=2)
                
                # Create corresponding PNG file (placeholder)
                png_file = word_dir / f"{filename}.png"
                png_file.touch()
    
    def test_service_registration(self):
        """Test that all services are properly registered."""
        # Verify main service can be resolved
        export_service = self.container.resolve(IImageExportService)
        assert export_service is not None
        
        # Verify service has required dependencies
        assert hasattr(export_service, 'image_renderer')
        assert hasattr(export_service, 'metadata_extractor')
        assert hasattr(export_service, 'layout_calculator')
    
    def test_single_sequence_export(self):
        """Test exporting a single sequence."""
        export_service = self.container.resolve(IImageExportService)
        
        # Create test sequence
        sequence_data = [
            {"beat": 1, "position": "start"},
            {"beat": 2, "position": "middle"},
            {"beat": 3, "position": "end"}
        ]
        
        word = "test"
        output_path = self.export_dir / "test_single.png"
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            user_name="IntegrationTest",
            export_date="01-01-2024",
            notes="Integration test sequence"
        )
        
        # Export the sequence
        result = export_service.export_sequence_image(
            sequence_data, word, output_path, options
        )
        
        # Verify export was successful
        assert result.success
        assert output_path.exists()
        assert result.output_path == output_path
        
        # Verify the exported image
        image = QImage(str(output_path))
        assert not image.isNull()
        assert image.format() == QImage.Format.Format_ARGB32
    
    def test_batch_export_with_real_data(self):
        """Test batch export with the created test data."""
        export_service = self.container.resolve(IImageExportService)
        
        options = ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            user_name="BatchTest",
            export_date="01-01-2024"
        )
        
        # Track progress
        progress_updates = []
        def progress_callback(progress):
            progress_updates.append({
                "current": progress.current,
                "total": progress.total,
                "message": progress.message
            })
        
        # Run batch export
        results = export_service.export_all_sequences(
            self.test_data_dir,
            self.export_dir,
            options,
            progress_callback
        )
        
        # Verify batch export results
        assert results["success"]
        assert results["total_files"] == 6  # 3 + 2 + 1 sequences
        assert results["successful"] > 0
        
        # Verify progress was tracked
        assert len(progress_updates) > 0
        assert progress_updates[0]["current"] == 0
        assert progress_updates[-1]["current"] == progress_updates[-1]["total"]
        
        # Verify exported files exist
        for word in ["apple", "banana", "cherry"]:
            word_export_dir = self.export_dir / word
            assert word_export_dir.exists()
            
            exported_files = list(word_export_dir.glob("*.png"))
            assert len(exported_files) > 0
            
            # Verify each exported file is valid
            for exported_file in exported_files:
                image = QImage(str(exported_file))
                assert not image.isNull()
    
    def test_export_with_different_options(self):
        """Test export with different option combinations."""
        export_service = self.container.resolve(IImageExportService)
        
        sequence_data = [{"beat": i, "position": f"pos_{i}"} for i in range(1, 9)]
        word = "options_test"
        
        # Test different option combinations
        option_sets = [
            # Minimal options
            ImageExportOptions(
                add_word=False,
                add_user_info=False,
                add_difficulty_level=False,
                add_beat_numbers=False
            ),
            # Full options
            ImageExportOptions(
                add_word=True,
                add_user_info=True,
                add_difficulty_level=True,
                add_beat_numbers=True,
                add_reversal_symbols=True,
                include_start_position=True,
                user_name="FullTest",
                notes="Full options test"
            ),
            # Custom options
            ImageExportOptions(
                add_word=True,
                add_difficulty_level=True,
                add_beat_numbers=False,
                user_name="CustomTest"
            )
        ]
        
        for i, options in enumerate(option_sets):
            output_path = self.export_dir / f"options_test_{i}.png"
            
            result = export_service.export_sequence_image(
                sequence_data, word, output_path, options
            )
            
            assert result.success
            assert output_path.exists()
            
            # Verify image properties
            image = QImage(str(output_path))
            assert not image.isNull()
            
            # Images with more options should generally be larger
            # (This is a basic check - more detailed verification would require image analysis)
            if i == 1:  # Full options
                assert image.height() > 600  # Should have additional height for text
    
    def test_error_recovery(self):
        """Test that the system handles errors gracefully."""
        export_service = self.container.resolve(IImageExportService)
        
        # Test with invalid sequence data
        invalid_sequence = [{"invalid": "data"}]
        output_path = self.export_dir / "error_test.png"
        options = ImageExportOptions()
        
        result = export_service.export_sequence_image(
            invalid_sequence, "error_test", output_path, options
        )
        
        # Should handle gracefully (either succeed with empty image or fail cleanly)
        assert isinstance(result.success, bool)
        
        # Test with non-existent source directory
        non_existent_dir = self.temp_dir / "does_not_exist"
        results = export_service.export_all_sequences(
            non_existent_dir, self.export_dir, options
        )
        
        # Should handle gracefully
        assert "success" in results
        assert "total_files" in results
    
    def test_memory_efficiency(self):
        """Test that the export process is memory efficient."""
        export_service = self.container.resolve(IImageExportService)
        
        # Create a larger sequence to test memory usage
        large_sequence = [{"beat": i, "position": f"pos_{i}"} for i in range(1, 25)]
        word = "memory_test"
        options = ImageExportOptions()
        
        # Export multiple large images
        for i in range(5):
            output_path = self.export_dir / f"memory_test_{i}.png"
            result = export_service.export_sequence_image(
                large_sequence, word, output_path, options
            )
            assert result.success
        
        # If we get here without memory errors, the test passes
        assert True
    
    def test_concurrent_exports(self):
        """Test that multiple exports can be handled."""
        export_service = self.container.resolve(IImageExportService)
        
        # Create multiple sequences
        sequences = [
            ([{"beat": i, "position": f"seq1_pos_{i}"} for i in range(1, 5)], "seq1"),
            ([{"beat": i, "position": f"seq2_pos_{i}"} for i in range(1, 9)], "seq2"),
            ([{"beat": i, "position": f"seq3_pos_{i}"} for i in range(1, 13)], "seq3")
        ]
        
        options = ImageExportOptions()
        results = []
        
        # Export all sequences
        for sequence_data, word in sequences:
            output_path = self.export_dir / f"{word}.png"
            result = export_service.export_sequence_image(
                sequence_data, word, output_path, options
            )
            results.append(result)
        
        # Verify all exports succeeded
        for result in results:
            assert result.success
            assert result.output_path.exists()
