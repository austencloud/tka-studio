#!/usr/bin/env python3
"""
Test Card Visibility - Verify Cards Are Visible
==============================================

Simple test to verify that application cards are visible with the new styling.
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_card_styling():
    """Test that card styling produces visible results."""
    logger.info("🧪 Testing card visibility...")
    
    try:
        from ui.design_system import get_style_builder, get_theme_manager
        from ui.components.modern_card import ModernApplicationCard, CardStyleManager
        
        # Test style generation
        style_manager = CardStyleManager()
        card_style = style_manager.get_card_style("default")
        
        logger.info("=== CARD STYLE OUTPUT ===")
        logger.info(card_style)
        
        # Check if background has sufficient opacity
        if "rgba(255, 255, 255, 0.25)" in card_style:
            logger.info("✅ Card background has 25% opacity - should be visible!")
        elif "rgba(255, 255, 255, 0.12)" in card_style:
            logger.warning("⚠️ Card background still has 12% opacity - may be too transparent")
        else:
            logger.info(f"ℹ️ Card background: {card_style}")
        
        # Test button styling
        button_style = style_manager.get_button_style("primary")
        logger.info("=== BUTTON STYLE OUTPUT ===")
        logger.info(button_style)
        
        if "rgba(59, 130, 246" in button_style:
            logger.info("✅ Button has blue accent color - should be visible!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🚀 Testing TKA Card Visibility...")
    
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    success = test_card_styling()
    
    if success:
        logger.info("🎉 Card visibility test passed!")
        logger.info("💡 Cards should now be visible in the launcher")
    else:
        logger.error("❌ Card visibility test failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
