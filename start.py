#!/usr/bin/env python3
"""
Smart Email Classifier Startup Script
Launches both backend and frontend services for development
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print the startup banner"""
    print("""
🧠 Smart Email Classifier with AI
====================================
Starting development environment...
    """)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import transformers
        import torch
        print("✅ Python dependencies: OK")
    except ImportError as e:
        print(f"❌ Python dependencies: Missing {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js: Not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js: Not found")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm: Not found")
            return False
    except FileNotFoundError:
        print("❌ npm: Not found")
        return False
    
    return True

def start_backend():
    """Start the Flask backend"""
    print("🚀 Starting Flask backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return None
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = '1'
    
    try:
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd=backend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ Backend started successfully")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("🌐 Starting React frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    # Check if node_modules exists, if not install dependencies
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return None
    
    try:
        process = subprocess.Popen(
            ['npm', 'start'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("✅ Frontend started successfully")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def wait_for_services():
    """Wait for services to be ready"""
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    print("""
🎉 Smart Email Classifier is ready!

📱 Frontend: http://localhost:3000
🔧 Backend:  http://localhost:5000
📊 API Docs: http://localhost:5000/api/health

Press Ctrl+C to stop all services
    """)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n🛑 Shutting down services...")
    sys.exit(0)

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start services
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        sys.exit(1)
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend")
        backend_process.terminate()
        sys.exit(1)
    
    # Wait for services
    wait_for_services()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
                
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal")
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main() 