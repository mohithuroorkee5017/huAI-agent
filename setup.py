#!/usr/bin/env python3
"""
HARIDWAR UNIVERSITY AI - Quick Setup Script
Installs dependencies and validates the environment
"""

import subprocess
import sys
import os
import platform

def print_banner():
    print("""
    ╔════════════════════════════════════════╗
    ║  HARIDWAR UNIVERSITY AI - Setup       ║
    ║  Advanced Voice-Based AI Assistant     ║
    ╚════════════════════════════════════════╝
    """)

def check_python_version():
    print("[1/5] Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} detected")
        return True
    else:
        print(f"✗ Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def install_dependencies():
    print("\n[2/5] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def install_pyaudio():
    print("\n[3/5] Installing PyAudio...")
    system = platform.system()
    
    if system == "Windows":
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pipwin'])
            subprocess.check_call([sys.executable, '-m', 'pipwin', 'install', 'pyaudio'])
            print("✓ PyAudio installed successfully")
            return True
        except:
            print("⚠ PyAudio installation failed. You may need to install manually.")
            return False
    else:
        print("⚠ PyAudio requires manual installation on non-Windows systems")
        return True

def validate_env():
    print("\n[4/5] Validating environment...")
    
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        return False
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'API_KEY' in content:
                print("✓ API key configured")
                return True
            else:
                print("✗ API key not found in .env")
                return False
    except:
        print("✗ Error reading .env file")
        return False

def check_ports():
    print("\n[5/5] Checking required ports...")
    
    import socket
    
    def is_port_open(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result != 0
    
    if is_port_open(5000):
        print("✓ Port 5000 is available")
        return True
    else:
        print("⚠ Port 5000 is in use. Change FLASK_PORT in .env")
        return True  # Not critical

def main():
    print_banner()
    
    checks = [
        ("Python Version", check_python_version),
        ("Installing Dependencies", install_dependencies),
        ("PyAudio Setup", install_pyaudio),
        ("Environment Config", validate_env),
        ("Port Check", check_ports),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append((name, False))
    
    print("\n" + "="*40)
    print("SETUP SUMMARY")
    print("="*40)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    if all(r for _, r in results):
        print("\n" + "✓"*20)
        print("✓ SETUP COMPLETE! ✓")
        print("✓"*20)
        print("\nTo start HUVOICE AGENT, run:")
        print("  python huvoice_agent.py")
        print("\nThen open: http://localhost:5000")
    else:
        print("\n⚠ Setup incomplete. Check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
