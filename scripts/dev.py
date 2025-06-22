#!/usr/bin/env python3
"""
Unified development script for TKA monorepo.
This script provides a single entry point for all development tasks.
"""

import subprocess
import sys
import os
import argparse
import threading
import time
import signal
from pathlib import Path


class TKADeveloper:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.processes = []
        self.running = True

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)

    def start_desktop(self):
        """Start PyQt desktop application."""
        print("🖥️  Starting desktop application...")
        desktop_path = self.root / "apps" / "desktop" / "modern"

        if not desktop_path.exists():
            print(f"❌ Desktop app path not found: {desktop_path}")
            return None

        os.chdir(desktop_path)
        process = subprocess.Popen([sys.executable, "main.py"])
        self.processes.append(process)
        print(f"✅ Desktop app started (PID: {process.pid})")
        return process

    def start_web(self):
        """Start SvelteKit web application."""
        print("🌐 Starting web application...")
        web_path = self.root / "apps" / "web"

        if not web_path.exists():
            print(f"❌ Web app path not found: {web_path}")
            return None

        os.chdir(web_path)
        process = subprocess.Popen(["npm", "run", "dev"])
        self.processes.append(process)
        print(f"✅ Web app started (PID: {process.pid})")
        return process

    def start_landing(self):
        """Start landing page application."""
        print("🏠 Starting landing page...")
        landing_path = self.root / "apps" / "landing"

        if not landing_path.exists():
            print(f"❌ Landing page path not found: {landing_path}")
            return None

        os.chdir(landing_path)
        process = subprocess.Popen(["npm", "run", "dev"])
        self.processes.append(process)
        print(f"✅ Landing page started (PID: {process.pid})")
        return process

    def start_animator(self):
        """Start animator application."""
        print("🎬 Starting animator...")
        animator_path = self.root / "apps" / "animator"

        if not animator_path.exists():
            print(f"❌ Animator path not found: {animator_path}")
            return None

        os.chdir(animator_path)
        process = subprocess.Popen(["npm", "run", "dev"])
        self.processes.append(process)
        print(f"✅ Animator started (PID: {process.pid})")
        return process

    def start_api(self):
        """Start FastAPI server."""
        print("🚀 Starting API server...")
        api_path = self.root / "apps" / "desktop" / "modern"

        if not api_path.exists():
            print(f"❌ API path not found: {api_path}")
            return None

        os.chdir(api_path)
        process = subprocess.Popen([sys.executable, "scripts/start_production_api.py"])
        self.processes.append(process)
        print(f"✅ API server started (PID: {process.pid})")
        return process

    def start_fullstack(self):
        """Start API + Web for full-stack development."""
        print("🔄 Starting full-stack development environment...")

        # Start API server
        api_process = self.start_api()
        if not api_process:
            print("❌ Failed to start API server")
            return

        # Wait for API to start
        print("⏳ Waiting for API server to initialize...")
        time.sleep(5)

        # Start web app
        web_process = self.start_web()
        if not web_process:
            print("❌ Failed to start web app")
            return

        print("\n✅ Full-stack environment running!")
        print("   🚀 API: http://localhost:8000")
        print("   🌐 Web: http://localhost:5173")
        print("   📚 API Docs: http://localhost:8000/docs")
        print("\n💡 Press Ctrl+C to stop all services")

        try:
            while self.running:
                time.sleep(1)
                # Check if processes are still running
                if api_process.poll() is not None:
                    print("⚠️  API server stopped unexpectedly")
                    break
                if web_process.poll() is not None:
                    print("⚠️  Web app stopped unexpectedly")
                    break
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def run_tests(self):
        """Run all tests."""
        print("🧪 Running all tests...")
        success = True

        # Python tests
        print("\n🐍 Running Python tests...")
        desktop_path = self.root / "apps" / "desktop"
        if desktop_path.exists():
            os.chdir(desktop_path)
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "modern/tests/", "-v", "--tb=short"]
            )
            if result.returncode != 0:
                print("❌ Python tests failed")
                success = False
            else:
                print("✅ Python tests passed")
        else:
            print("⚠️  Desktop app not found, skipping Python tests")

        # Web tests
        print("\n🌐 Running Web tests...")
        web_path = self.root / "apps" / "web"
        if web_path.exists():
            os.chdir(web_path)
            # Check if npm test script exists
            package_json = web_path / "package.json"
            if package_json.exists():
                result = subprocess.run(["npm", "test"])
                if result.returncode != 0:
                    print("❌ Web tests failed")
                    success = False
                else:
                    print("✅ Web tests passed")
            else:
                print("⚠️  package.json not found, skipping web tests")
        else:
            print("⚠️  Web app not found, skipping web tests")

        if success:
            print("\n🎉 All tests passed!")
        else:
            print("\n💥 Some tests failed!")

        return success

    def build_all(self):
        """Build all applications."""
        print("🔨 Building all applications...")
        success = True

        # Build web apps
        for app in ["web", "landing", "animator"]:
            print(f"\n🏗️  Building {app}...")
            app_path = self.root / "apps" / app
            if app_path.exists():
                os.chdir(app_path)
                result = subprocess.run(["npm", "run", "build"])
                if result.returncode != 0:
                    print(f"❌ Failed to build {app}")
                    success = False
                else:
                    print(f"✅ {app} built successfully")
            else:
                print(f"⚠️  {app} not found, skipping")

        # Build desktop (if build script exists)
        print("\n🖥️  Building desktop...")
        desktop_path = self.root / "apps" / "desktop"
        build_script = desktop_path / "scripts" / "build.py"
        if build_script.exists():
            os.chdir(desktop_path)
            result = subprocess.run([sys.executable, "scripts/build.py"])
            if result.returncode != 0:
                print("❌ Failed to build desktop")
                success = False
            else:
                print("✅ Desktop built successfully")
        else:
            print("⚠️  Desktop build script not found, skipping")

        if success:
            print("\n🎉 All applications built successfully!")
        else:
            print("\n💥 Some builds failed!")

        return success

    def setup_environment(self):
        """Set up development environment."""
        print("⚙️  Setting up development environment...")

        # Install root dependencies
        print("\n📦 Installing root dependencies...")
        os.chdir(self.root)
        subprocess.run(["npm", "install"])

        # Install Python dependencies (if requirements exist)
        desktop_path = self.root / "apps" / "desktop"
        if desktop_path.exists():
            print("\n🐍 Setting up Python environment...")
            os.chdir(desktop_path)

            # Check for different Python dependency files
            if (desktop_path / "requirements.txt").exists():
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
                )
            elif (desktop_path / "pyproject.toml").exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
            else:
                print("⚠️  No Python requirements found")

        # Install Node dependencies for all web apps
        for app in ["web", "landing", "animator"]:
            app_path = self.root / "apps" / app
            if app_path.exists():
                print(f"\n📦 Installing dependencies for {app}...")
                os.chdir(app_path)
                subprocess.run(["npm", "install"])
            else:
                print(f"⚠️  {app} not found, skipping")

        print("\n✅ Development environment setup complete!")
        print("\n🚀 You can now run:")
        print("   python scripts/dev.py fullstack  # Start API + Web")
        print("   python scripts/dev.py desktop    # Start desktop app")
        print("   python scripts/dev.py test       # Run all tests")

    def cleanup(self):
        """Clean up running processes."""
        if not self.processes:
            return

        print("🧹 Cleaning up processes...")
        for process in self.processes:
            if process.poll() is None:
                try:
                    process.terminate()
                    # Wait a bit for graceful shutdown
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't terminate gracefully
                    process.kill()
                except Exception as e:
                    print(f"⚠️  Error terminating process {process.pid}: {e}")

        self.processes.clear()
        print("✅ Cleanup complete")


def main():
    """Main entry point for the development script."""
    parser = argparse.ArgumentParser(
        description="TKA Development Helper - Unified development script for TKA monorepo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/dev.py setup      # Set up development environment
  python scripts/dev.py fullstack  # Start API + Web for full-stack development
  python scripts/dev.py desktop    # Start desktop application only
  python scripts/dev.py web        # Start web application only
  python scripts/dev.py api        # Start API server only
  python scripts/dev.py test       # Run all tests
  python scripts/dev.py build      # Build all applications
  python scripts/dev.py clean      # Clean up running processes
        """,
    )

    parser.add_argument(
        "command",
        choices=[
            "desktop",
            "web",
            "landing",
            "animator",
            "api",
            "fullstack",
            "test",
            "build",
            "setup",
            "clean",
        ],
        help="Command to execute",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # Create developer instance
    dev = TKADeveloper()

    try:
        print(f"🚀 TKA Development Helper - Running: {args.command}")
        print(f"📁 Working directory: {dev.root}")
        print()

        if args.command == "desktop":
            process = dev.start_desktop()
            if process:
                process.wait()
        elif args.command == "web":
            process = dev.start_web()
            if process:
                process.wait()
        elif args.command == "landing":
            process = dev.start_landing()
            if process:
                process.wait()
        elif args.command == "animator":
            process = dev.start_animator()
            if process:
                process.wait()
        elif args.command == "api":
            process = dev.start_api()
            if process:
                process.wait()
        elif args.command == "fullstack":
            dev.start_fullstack()
        elif args.command == "test":
            success = dev.run_tests()
            sys.exit(0 if success else 1)
        elif args.command == "build":
            success = dev.build_all()
            sys.exit(0 if success else 1)
        elif args.command == "setup":
            dev.setup_environment()
        elif args.command == "clean":
            dev.cleanup()

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        dev.cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        dev.cleanup()
        sys.exit(1)
    finally:
        dev.cleanup()
        print("\n👋 Development session ended")


if __name__ == "__main__":
    main()
