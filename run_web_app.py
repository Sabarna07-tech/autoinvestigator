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
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Set environment variables if needed
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')

def main():
    """Main launcher function"""
    print("🚀 Starting AutoInvestigator Web Application...")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to setup dependencies. Exiting.")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    try:
        # Import and run the web app
        from client.web_app import app
        
        print("✅ Web application loaded successfully!")
        print("🌐 Starting server on http://localhost:5000")
        print("📱 Landing page: http://localhost:5000")
        print("🔍 Investigation interface: http://localhost:5000/investigate")
        print("\n" + "="*50)
        print("Press Ctrl+C to stop the server")
        print("="*50 + "\n")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open('http://localhost:5000')
            except:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Disable reloader to avoid duplicate processes
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

if __name__ == '__main__':
    main() 