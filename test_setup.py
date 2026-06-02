"""
HUVOICE AGENT - Test Suite
Validates that all components are working correctly
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    tests = [
        ('flask', 'Flask'),
        ('requests', 'HTTP Client'),
        ('speech_recognition', 'Speech Recognition'),
        ('pyttsx3', 'Text-to-Speech'),
        ('bs4', 'BeautifulSoup'),
        ('dotenv', 'Python-dotenv'),
    ]
    
    failed = []
    
    for module, name in tests:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            failed.append(module)
    
    return len(failed) == 0

def test_env_file():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('API_KEY')
        if api_key:
            print(f"  ✓ API Key found: {api_key[:20]}...")
            return True
        else:
            print("  ✗ API Key not configured")
            return False
    except Exception as e:
        print(f"  ✗ Error reading .env: {e}")
        return False

def test_project_structure():
    """Test project file structure"""
    print("\nTesting project structure...")
    
    required_files = [
        ('huvoice_agent.py', 'Main agent'),
        ('requirements.txt', 'Dependencies'),
        ('.env', 'Configuration'),
        ('templates/index.html', 'Web interface'),
        ('static/style.css', 'Styling'),
        ('static/script.js', 'Frontend logic'),
        ('README.md', 'Documentation'),
    ]
    
    all_present = True
    
    for file_path, description in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {description}")
        else:
            print(f"  ✗ {description} - MISSING")
            all_present = False
    
    return all_present

def test_network():
    """Test network connectivity"""
    print("\nTesting network connectivity...")
    
    try:
        import requests
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            print("  ✓ Internet connection OK")
            return True
        else:
            print("  ✗ Google search may not work")
            return False
    except Exception as e:
        print(f"  ✗ Network error: {e}")
        print("  Note: Voice input/output requires internet")
        return False

def test_audio():
    """Test audio capabilities"""
    print("\nTesting audio capabilities...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("  ✓ Text-to-Speech engine initialized")
    except Exception as e:
        print(f"  ✗ Text-to-Speech error: {e}")
        return False
    
    try:
        import speech_recognition
        recognizer = speech_recognition.Recognizer()
        print("  ✓ Speech Recognition initialized")
    except Exception as e:
        print(f"  ✗ Speech Recognition error: {e}")
        return False
    
    return True

def main():
    print("\n" + "="*50)
    print("HUVOICE AGENT - Diagnostic Tests")
    print("="*50 + "\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Environment Config", test_env_file),
        ("Project Structure", test_project_structure),
        ("Network Connectivity", test_network),
        ("Audio Capabilities", test_audio),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("TEST RESULTS")
    print("="*50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! HUVOICE AGENT is ready to use.")
        print("\nTo start the agent, run:")
        print("  python huvoice_agent.py")
        print("\nOr use the startup script:")
        print("  Windows: run.bat")
        print("  Linux/Mac: bash run.sh")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("\nInstall missing dependencies with:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
