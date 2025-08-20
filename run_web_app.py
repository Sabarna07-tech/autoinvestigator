#!/usr/bin/env python3
"""
AutoInvestigator Web Application Launcher
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path
import contextlib

# Automatically allow HTTP for OAuthlib in local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for local dev, never in production!


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'flask-cors']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False

    return True


def setup_environment():
    """Setup environment variables and paths"""
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')


def main():
    """Main launcher function"""
    print("🚀 Starting AutoInvestigator Web Application...")

    if not check_dependencies():
        print("❌ Failed to setup dependencies. Exiting.")
        sys.exit(1)

    setup_environment()

    server_proc = None
    try:
        from client.web_app import app

        server_port = os.environ.get('SERVER_PORT', '8000')
        server_env = {**os.environ, 'SERVER_PORT': server_port}
        server_proc = subprocess.Popen([sys.executable, 'server.py'], env=server_env)
        print(f"🛠 API server started on http://localhost:{server_port}")

        print("✅ Web application loaded successfully!")
        print("🌐 Web interface: http://localhost:5000")
        print("🔍 Investigation interface: http://localhost:5000/investigate")
        print("\n" + "=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50 + "\n")

        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open('http://localhost:5000')
            except Exception:
                pass

        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False
        )

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down AutoInvestigator...")
        print("✅ Server stopped successfully!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        if server_proc:
            server_proc.terminate()
            with contextlib.suppress(Exception):
                server_proc.wait(timeout=5)


if __name__ == '__main__':
    main()
