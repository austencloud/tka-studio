"""
Screenshot-based Thumbnail Height Analysis

This test captures screenshots of the running TKA app and analyzes
thumbnail heights using image processing techniques.
"""

import sys
import os
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

# Add TKA paths
tka_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(tka_root))


class ScreenshotThumbnailAnalyzer:
    """Analyze thumbnail heights using screenshots."""
    
    def __init__(self):
        self.tka_root = Path(__file__).parent.parent.parent
        self.screenshots_dir = Path(__file__).parent / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        self.analysis_results = {}
        
    def capture_browse_tab(self) -> Optional[str]:
        """Capture screenshot of the browse tab."""
        try:
            # Use built-in Windows screenshot capability
            import pyautogui
            
            # Wait for user to position window
            print("📸 Preparing to capture screenshot...")
            print("Please ensure:")
            print("1. TKA app is running")
            print("2. Browse tab is open")
            print("3. Sequences are loaded")
            print("4. App window is visible and unobstructed")
            
            input("Press Enter when ready to capture...")
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot_path = self.screenshots_dir / f"browse_tab_{int(time.time())}.png"
            screenshot.save(screenshot_path)
            
            print(f"✅ Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
            
        except ImportError:
            print("❌ pyautogui not available. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui"], check=True)
                print("✅ pyautogui installed. Please run again.")
                return None
            except subprocess.CalledProcessError:
                print("❌ Failed to install pyautogui")
                return None
        except Exception as e:
            print(f"❌ Error capturing screenshot: {e}")
            return None
    
    def analyze_screenshot(self, screenshot_path: str) -> Dict:
        """Analyze thumbnail heights from screenshot."""
        try:
            # Load screenshot
            img = cv2.imread(screenshot_path)
            if img is None:
                print(f"❌ Could not load screenshot: {screenshot_path}")
                return {}
                
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect rectangular regions (thumbnails)
            rectangles = self._detect_thumbnail_rectangles(gray)
            
            # Analyze each rectangle
            analysis = {
                "screenshot_path": screenshot_path,
                "total_thumbnails": len(rectangles),
                "thumbnails": []
            }
            
            for i, rect in enumerate(rectangles):
                x, y, w, h = rect
                thumbnail_analysis = self._analyze_thumbnail_region(img, gray, rect, i)
                analysis["thumbnails"].append(thumbnail_analysis)
                
            # Calculate statistics
            if analysis["thumbnails"]:
                heights = [t["height"] for t in analysis["thumbnails"]]
                widths = [t["width"] for t in analysis["thumbnails"]]
                
                analysis["statistics"] = {
                    "avg_height": np.mean(heights),
                    "avg_width": np.mean(widths),
                    "height_std": np.std(heights),
                    "width_std": np.std(widths),
                    "min_height": np.min(heights),
                    "max_height": np.max(heights),
                    "height_range": np.max(heights) - np.min(heights)
                }
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing screenshot: {e}")
            return {}
    
    def _detect_thumbnail_rectangles(self, gray_img: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect rectangular regions that look like thumbnails."""
        # Apply edge detection
        edges = cv2.Canny(gray_img, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangles = []
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's roughly rectangular
            if len(approx) >= 4:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter based on size (thumbnails should be reasonably sized)
                if 100 < w < 400 and 80 < h < 300:
                    # Check aspect ratio (thumbnails shouldn't be too thin or wide)
                    aspect_ratio = w / h
                    if 0.8 < aspect_ratio < 2.0:
                        rectangles.append((x, y, w, h))
        
        # Sort by position (top to bottom, left to right)
        rectangles.sort(key=lambda r: (r[1], r[0]))
        
        return rectangles
    
    def _analyze_thumbnail_region(self, img: np.ndarray, gray_img: np.ndarray, 
                                 rect: Tuple[int, int, int, int], index: int) -> Dict:
        """Analyze a specific thumbnail region."""
        x, y, w, h = rect
        
        # Extract thumbnail region
        thumbnail_region = img[y:y+h, x:x+w]
        gray_region = gray_img[y:y+h, x:x+w]
        
        # Try to detect different components within the thumbnail
        # This is approximate - actual implementation would need more sophisticated image analysis
        
        analysis = {
            "index": index,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "area": w * h,
            "aspect_ratio": w / h,
            "components": self._detect_thumbnail_components(gray_region)
        }
        
        return analysis
    
    def _detect_thumbnail_components(self, gray_region: np.ndarray) -> Dict:
        """Detect components within a thumbnail (text, image, etc.)."""
        h, w = gray_region.shape
        
        # Divide into rough regions
        top_region = gray_region[0:h//4, :]  # Word label area
        middle_region = gray_region[h//4:3*h//4, :]  # Image area
        bottom_region = gray_region[3*h//4:, :]  # Info area
        
        # Analyze each region
        components = {
            "top_region": {
                "height": h//4,
                "has_text": self._has_text_content(top_region),
                "avg_intensity": np.mean(top_region)
            },
            "middle_region": {
                "height": h//2,
                "has_image": self._has_image_content(middle_region),
                "avg_intensity": np.mean(middle_region)
            },
            "bottom_region": {
                "height": h//4,
                "has_text": self._has_text_content(bottom_region),
                "avg_intensity": np.mean(bottom_region)
            }
        }
        
        return components
    
    def _has_text_content(self, region: np.ndarray) -> bool:
        """Check if region likely contains text."""
        # Simple heuristic: text regions have more variation in intensity
        return np.std(region) > 20
    
    def _has_image_content(self, region: np.ndarray) -> bool:
        """Check if region likely contains an image."""
        # Simple heuristic: image regions have structured content
        edges = cv2.Canny(region, 50, 150)
        return np.sum(edges > 0) > region.size * 0.1
    
    def create_analysis_report(self, analysis: Dict) -> str:
        """Create a detailed analysis report."""
        if not analysis:
            return "No analysis data available"
            
        report = []
        report.append("📊 THUMBNAIL HEIGHT ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Basic stats
        report.append(f"Screenshot: {analysis.get('screenshot_path', 'N/A')}")
        report.append(f"Total thumbnails detected: {analysis.get('total_thumbnails', 0)}")
        
        # Statistics
        if "statistics" in analysis:
            stats = analysis["statistics"]
            report.append(f"Average height: {stats['avg_height']:.1f}px")
            report.append(f"Average width: {stats['avg_width']:.1f}px")
            report.append(f"Height range: {stats['min_height']:.0f} - {stats['max_height']:.0f}px")
            report.append(f"Height variation: {stats['height_std']:.1f}px")
            
            # Assessment
            if stats['height_std'] > 20:
                report.append("⚠️ HIGH height variation detected")
            elif stats['height_std'] > 10:
                report.append("⚠️ MODERATE height variation detected")
            else:
                report.append("✅ Low height variation - good consistency")
        
        # Individual thumbnails
        if "thumbnails" in analysis:
            report.append(f"\n📋 INDIVIDUAL THUMBNAILS:")
            for thumb in analysis["thumbnails"]:
                report.append(f"  Thumbnail {thumb['index']}: {thumb['width']}x{thumb['height']}px")
                
                # Component analysis
                if "components" in thumb:
                    comp = thumb["components"]
                    report.append(f"    Top region: {comp['top_region']['height']}px")
                    report.append(f"    Middle region: {comp['middle_region']['height']}px")
                    report.append(f"    Bottom region: {comp['bottom_region']['height']}px")
        
        return "\n".join(report)
    
    def save_analysis(self, analysis: Dict, filename: str = None) -> str:
        """Save analysis results to file."""
        if not filename:
            filename = f"thumbnail_analysis_{int(time.time())}.json"
            
        results_path = self.screenshots_dir / filename
        
        with open(results_path, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
            
        return str(results_path)
    
    def run_full_analysis(self) -> bool:
        """Run the complete screenshot analysis."""
        print("📸 TKA Thumbnail Height Analysis")
        print("=" * 50)
        
        # Capture screenshot
        screenshot_path = self.capture_browse_tab()
        if not screenshot_path:
            return False
            
        # Analyze screenshot
        print("🔍 Analyzing screenshot...")
        analysis = self.analyze_screenshot(screenshot_path)
        
        if not analysis:
            print("❌ Analysis failed")
            return False
            
        # Save results
        results_path = self.save_analysis(analysis)
        print(f"💾 Analysis saved: {results_path}")
        
        # Create report
        report = self.create_analysis_report(analysis)
        print(f"\n{report}")
        
        # Save report
        report_path = self.screenshots_dir / f"analysis_report_{int(time.time())}.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"📄 Report saved: {report_path}")
        
        return True


def install_requirements():
    """Install required packages for image analysis."""
    required_packages = [
        "pillow",
        "opencv-python",
        "numpy",
        "pyautogui"
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)


def main():
    """Main function."""
    print("🔧 Checking requirements...")
    
    try:
        install_requirements()
        print("✅ Requirements satisfied")
    except Exception as e:
        print(f"❌ Failed to install requirements: {e}")
        return
    
    # Run analysis
    analyzer = ScreenshotThumbnailAnalyzer()
    
    print("\n🎯 Starting thumbnail height analysis...")
    print("Make sure TKA app is running with browse tab open!")
    
    success = analyzer.run_full_analysis()
    
    if success:
        print("\n✅ Analysis completed successfully!")
        print(f"📁 Results saved in: {analyzer.screenshots_dir}")
    else:
        print("\n❌ Analysis failed")


if __name__ == "__main__":
    main()
