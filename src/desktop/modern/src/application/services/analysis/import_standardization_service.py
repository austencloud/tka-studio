"""
Import Standardization Service

Pure service for standardizing import patterns in Python files.
Extracted from ImportStandardizer to follow single responsibility principle.

This service handles:
- Import pattern fixing and standardization
- File content modification
- Backup creation and safety checks
- Batch standardization operations

Uses dependency injection for file system and analysis services.
"""

import re
import logging
from pathlib import Path
from typing import Dict, Union

from core.interfaces.organization_services import (
    IImportStandardizationService,
    IFileSystemService,
    IImportAnalysisService,
    ImportStandardizationReport,
)

logger = logging.getLogger(__name__)


class ImportStandardizationService(IImportStandardizationService):
    """
    Pure service for standardizing import patterns in Python files.

    Handles file modification operations with proper safety checks
    and backup creation. Uses dependency injection for file operations.
    """

    def __init__(
        self,
        file_system_service: IFileSystemService,
        import_analysis_service: IImportAnalysisService,
    ):
        """
        Initialize the import standardization service.

        Args:
            file_system_service: Service for file system operations
            import_analysis_service: Service for import analysis
        """
        self.file_system_service = file_system_service
        self.import_analysis_service = import_analysis_service

        # Standardization patterns (regex replacements)
        self.standardization_patterns = [
            # Remove src. prefix
            (r"^from src\.", "from ", re.MULTILINE),
            # Remove modern.src. prefix
            (r"^from modern\.src\.", "from ", re.MULTILINE),
            # Remove modern. prefix
            (r"^from modern\.", "from ", re.MULTILINE),
            # Fix double dots in relative imports (common mistake)
            (r"^from \.\.\.\.+", "from ...", re.MULTILINE),
        ]

    def fix_file_imports(self, file_path: Path, dry_run: bool = True) -> bool:
        """
        Fix import patterns in a single file.

        Args:
            file_path: Path to the file to fix
            dry_run: If True, only show what would be changed

        Returns:
            True if fixes were applied (or would be applied in dry_run)
        """
        try:
            # Validate file before processing
            if not self.file_system_service.validate_file_path(file_path):
                logger.warning(f"Invalid file path, skipping: {file_path}")
                return False

            content = self.file_system_service.read_file(file_path)
            original_content = content

            # Apply standardization patterns
            for pattern, replacement, flags in self.standardization_patterns:
                content = re.sub(pattern, replacement, content, flags=flags)

            # Check if any changes were made
            if content != original_content:
                if dry_run:
                    logger.info(f"Would fix imports in: {file_path}")
                    self._log_changes(original_content, content, file_path)
                    return True
                else:
                    # Create backup before modifying
                    backup_path = self.file_system_service.backup_file(file_path)
                    logger.info(f"Created backup: {backup_path}")

                    # Write the fixed content
                    self.file_system_service.write_file(file_path, content)
                    logger.info(f"Fixed imports in: {file_path}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error fixing imports in {file_path}: {e}")
            return False

    def standardize_codebase(
        self, dry_run: bool = True
    ) -> Dict[str, Union[int, float]]:
        """
        Standardize imports across the entire codebase.

        Args:
            dry_run: If True, only show what would be changed

        Returns:
            Dictionary with fix statistics
        """
        # Get analysis report to identify files needing fixes
        report = self.import_analysis_service.analyze_codebase()

        fixed_files = 0
        total_fixes = 0
        errors = 0

        logger.info(
            f"Starting import standardization {'simulation' if dry_run else 'execution'}..."
        )

        for file_path in report.files_needing_fixes:
            try:
                if self.fix_file_imports(file_path, dry_run):
                    fixed_files += 1
                    total_fixes += 1
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                errors += 1

        # Log summary
        logger.info(
            f"Import standardization {'simulation' if dry_run else 'execution'} complete:"
        )
        logger.info(f"  - Files {'would be' if dry_run else ''} fixed: {fixed_files}")
        logger.info(
            f"  - Total fixes {'would be' if dry_run else ''} applied: {total_fixes}"
        )
        if errors > 0:
            logger.warning(f"  - Errors encountered: {errors}")

        # Estimate compliance improvement
        compliance_improvement = self._estimate_compliance_improvement(report)

        return {
            "files_fixed": fixed_files,
            "total_fixes": total_fixes,
            "errors": errors,
            "compliance_improvement": compliance_improvement,
            "dry_run": dry_run,
        }

    def _log_changes(self, original: str, modified: str, file_path: Path) -> None:
        """
        Log the changes that would be made to a file.

        Args:
            original: Original file content
            modified: Modified file content
            file_path: Path to the file
        """
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()

        changes_found = False
        for i, (orig_line, mod_line) in enumerate(zip(original_lines, modified_lines)):
            if orig_line != mod_line:
                if not changes_found:
                    logger.info(f"Changes for {file_path}:")
                    changes_found = True
                logger.info(f"  Line {i+1}: '{orig_line}' -> '{mod_line}'")

    def _estimate_compliance_improvement(
        self, report: ImportStandardizationReport
    ) -> float:
        """
        Estimate compliance improvement after standardization.

        Args:
            report: Import standardization report

        Returns:
            Estimated compliance improvement percentage
        """
        # Estimate improvement based on common violations
        src_prefix_violations = report.common_violations.get("src_prefix_violations", 0)
        total_violations = sum(report.common_violations.values())

        if total_violations == 0:
            return 0.0

        # Estimate that fixing src. prefix violations improves compliance by ~20%
        improvement = (src_prefix_violations / total_violations) * 20.0
        return min(improvement, 25.0)  # Cap at 25% improvement

    def validate_standardization_patterns(self) -> dict:
        """
        Validate that standardization patterns are working correctly.

        Returns:
            Dictionary with validation results
        """
        test_cases = [
            (
                "from domain.models import BeatData",
                "from domain.models import BeatData",
            ),
            (
                "from modern.src.application import Service",
                "from application import Service",
            ),
            (
                "from modern.presentation import Component",
                "from presentation import Component",
            ),
            (
                "from ....deep.import import Something",
                "from ...deep.import import Something",
            ),
        ]

        results = {"valid": True, "test_results": [], "issues": []}

        for original, expected in test_cases:
            modified = original
            for pattern, replacement, flags in self.standardization_patterns:
                modified = re.sub(pattern, replacement, modified, flags=flags)

            test_result = {
                "original": original,
                "expected": expected,
                "actual": modified,
                "passed": modified == expected,
            }

            results["test_results"].append(test_result)

            if not test_result["passed"]:
                results["valid"] = False
                results["issues"].append(
                    f"Pattern failed: '{original}' -> '{modified}' (expected: '{expected}')"
                )

        return results

    def get_standardization_preview(self, file_path: Path) -> dict:
        """
        Get a preview of what standardization would do to a file.

        Args:
            file_path: Path to preview

        Returns:
            Dictionary with preview information
        """
        try:
            if not self.file_system_service.validate_file_path(file_path):
                return {"error": "Invalid file path"}

            content = self.file_system_service.read_file(file_path)
            original_content = content

            # Apply standardization patterns
            for pattern, replacement, flags in self.standardization_patterns:
                content = re.sub(pattern, replacement, content, flags=flags)

            # Find specific changes
            original_lines = original_content.splitlines()
            modified_lines = content.splitlines()

            changes = []
            for i, (orig_line, mod_line) in enumerate(
                zip(original_lines, modified_lines)
            ):
                if orig_line != mod_line:
                    changes.append(
                        {
                            "line_number": i + 1,
                            "original": orig_line.strip(),
                            "modified": mod_line.strip(),
                        }
                    )

            return {
                "file_path": str(file_path),
                "has_changes": content != original_content,
                "changes_count": len(changes),
                "changes": changes,
                "preview_lines": content.splitlines()[:20],  # First 20 lines preview
            }

        except Exception as e:
            logger.error(f"Error generating preview for {file_path}: {e}")
            return {"error": str(e)}

    def rollback_changes(self, file_path: Path) -> bool:
        """
        Rollback changes by restoring from backup.

        Args:
            file_path: Path to rollback

        Returns:
            True if rollback was successful
        """
        backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")

        try:
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False

            backup_content = self.file_system_service.read_file(backup_path)
            self.file_system_service.write_file(file_path, backup_content)

            logger.info(f"Successfully rolled back changes to: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error rolling back {file_path}: {e}")
            return False
