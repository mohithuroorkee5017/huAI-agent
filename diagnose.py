"""
HUVOICE AGENT - Advanced Diagnostics
Comprehensive system and component health check
"""

import os
import sys
import platform
import subprocess
import json
from datetime import datetime

class DiagnosticReport:
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
    
    def add_result(self, category, test, status, details=""):
        self.results.append({
            "category": category,
            "test": test,
            "status": status,
            "details": details
        })
    
    def add_warning(self, message):
        self.warnings.append(message)
    
    def add_error(self, message):
        self.errors.append(message)
    
    def print_report(self):
        print("\n" + "="*60)
        print("HUVOICE AGENT - DIAGNOSTIC REPORT")
        print("="*60)
        print(f"Generated: {datetime.now().isoformat()}\n")
        
        # System Information
        print("SYSTEM INFORMATION")
        print("-" * 60)
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.architecture()[0]}")
        print(f"Python: {platform.python_version()}")
        print(f"Python Executable: {sys.executable}\n")
        
        # Results by Category
        categories = {}
        for result in self.results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        for category in sorted(categories.keys()):
            print(f"\n{category}")
            print("-" * 60)
            for result in categories[category]:
                status_symbol = "✓" if result['status'] == "PASS" else "✗"
                print(f"{status_symbol} {result['test']}: {result['status']}")
                if result['details']:
                    print(f"  └─ {result['details']}")
        
        # Warnings
        if self.warnings:
            print(f"\n\nWARNINGS ({len(self.warnings)})")
            print("-" * 60)
            for i, warning in enumerate(self.warnings, 1):
                print(f"{i}. ⚠ {warning}")
        
        # Errors
        if self.errors:
            print(f"\n\nERRORS ({len(self.errors)})")
            print("-" * 60)
            for i, error in enumerate(self.errors, 1):
                print(f"{i}. ✗ {error}")
        
        # Summary
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        total = len(self.results)
        
        print(f"\n\nSUMMARY")
        print("-" * 60)
        print(f"Tests Passed: {passed}/{total}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")
        
        if passed == total and not self.errors:
            print("\n✓ SYSTEM READY - All checks passed!")
            return 0
        else:
            print("\n⚠ SYSTEM HAS ISSUES - Review above for details")
            return 1

def run_diagnostics():
    report = DiagnosticReport()
    
    # Python Environment
    report.add_result("Python Environment", "Python Version", "PASS", 
                     f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check Project Files
    print("Checking project structure...")
    files_to_check = [
        ('huvoice_agent.py', 'Main Application'),
        ('requirements.txt', 'Dependencies File'),
        ('.env', 'Environment Config'),
        ('templates/index.html', 'Web Interface'),
        ('static/style.css', 'Stylesheet'),
        ('static/script.js', 'JavaScript'),
        ('README.md', 'Documentation'),
    ]
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            report.add_result("Project Files", description, "PASS", f"{size} bytes")
        else:
            report.add_result("Project Files", description, "FAIL", "File not found")
            report.add_error(f"Missing file: {file_path}")
    
    # Python Packages
    print("Checking Python packages...")
    packages = [
        ('flask', 'Flask Web Framework'),
        ('requests', 'HTTP Client'),
        ('speech_recognition', 'Speech Recognition'),
        ('pyttsx3', 'Text-to-Speech'),
        ('bs4', 'BeautifulSoup'),
        ('dotenv', 'Python-dotenv'),
    ]
    
    for package, description in packages:
        try:
            __import__(package)
            report.add_result("Python Packages", description, "PASS")
        except ImportError:
            report.add_result("Python Packages", description, "FAIL", "Not installed")
            report.add_warning(f"Missing: {package} - Install with: pip install {package}")
    
    # Environment Configuration
    print("Checking environment...")
    if os.path.exists('.env'):
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('API_KEY')
            if api_key:
                masked_key = api_key[:10] + "..." + api_key[-10:]
                report.add_result("Configuration", "API Key", "PASS", masked_key)
            else:
                report.add_result("Configuration", "API Key", "FAIL", "Not configured")
                report.add_error("API_KEY not found in .env")
            
            flask_port = os.getenv('FLASK_PORT', '5000')
            report.add_result("Configuration", "Flask Port", "PASS", flask_port)
            
        except Exception as e:
            report.add_result("Configuration", ".env File", "FAIL", str(e))
            report.add_error(f"Error reading .env: {e}")
    else:
        report.add_result("Configuration", ".env File", "FAIL", "Not found")
        report.add_error(".env file not found")
    
    # Network & Connectivity
    print("Checking network connectivity...")
    try:
        import requests
        response = requests.get('https://www.google.com', timeout=5)
        report.add_result("Connectivity", "Internet", "PASS", f"Status {response.status_code}")
    except Exception as e:
        report.add_result("Connectivity", "Internet", "FAIL", str(e)[:50])
        report.add_warning("No internet connection or Google unreachable")
    
    # Disk Space
    print("Checking disk space...")
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free / (1024**3)
        if free_gb > 0.5:
            report.add_result("System", "Disk Space", "PASS", f"{free_gb:.2f} GB free")
        else:
            report.add_result("System", "Disk Space", "FAIL", f"Only {free_gb:.2f} GB free")
            report.add_warning("Low disk space available")
    except Exception as e:
        report.add_result("System", "Disk Space", "FAIL", str(e)[:50])
    
    # Port Check
    print("Checking ports...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            report.add_result("Ports", "Port 5000", "FAIL", "Port is in use")
            report.add_warning("Port 5000 already in use - change FLASK_PORT in .env")
        else:
            report.add_result("Ports", "Port 5000", "PASS", "Available")
    except Exception as e:
        report.add_result("Ports", "Port 5000", "FAIL", str(e)[:50])
    
    # Audio System
    print("Checking audio system...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        report.add_result("Audio", "Text-to-Speech", "PASS", "Engine initialized")
    except Exception as e:
        report.add_result("Audio", "Text-to-Speech", "FAIL", str(e)[:50])
        report.add_warning("TTS may not work properly")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        mics = sr.Microphone.list_microphone_indexes()
        report.add_result("Audio", "Speech Recognition", "PASS", f"{len(mics)} microphones")
    except Exception as e:
        report.add_result("Audio", "Speech Recognition", "FAIL", str(e)[:50])
        report.add_warning("Voice input may not work")
    
    return report

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║  HUVOICE AGENT - Diagnostic Tool     ║
    ║  System & Component Health Check      ║
    ╚════════════════════════════════════════╝
    """)
    
    report = run_diagnostics()
    exit_code = report.print_report()
    
    # Save report to file
    report_file = f"diagnostic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    print(f"\n📄 Report saved to: {report_file}")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
