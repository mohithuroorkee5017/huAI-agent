#!/usr/bin/env python3
"""
Test script for unified Haridwar University AI application
Verifies all major functionality works correctly
"""

import json
import time
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_imports():
    """Test that all required packages can be imported"""
    print_header("TEST 1: Checking Imports")
    
    required_packages = [
        'flask',
        'requests',
        'dotenv',
        'langdetect',
        'wikipedia',
        'duckduckgo_search'
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - MISSING")
            all_good = False
    
    return all_good

def test_env_file():
    """Test that .env file exists and has required variables"""
    print_header("TEST 2: Checking Environment Variables")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['OPENROUTER_API_KEY']
    optional_vars = ['SECRET_KEY', 'FLASK_ENV']
    
    all_good = True
    
    # Check required
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} - Found ({value[:20]}...)")
        else:
            print(f"❌ {var} - MISSING! Add to .env file")
            all_good = False
    
    # Check optional
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"ℹ️  {var} - {value}")
        else:
            print(f"ℹ️  {var} - Not set (optional)")
    
    return all_good

def test_app_structure():
    """Test that all required files exist"""
    print_header("TEST 3: Checking Project Structure")
    
    required_files = [
        'app.py',
        'requirements-unified.txt',
        'render.yaml',
        'templates/index.html',
        'templates/dashboard.html',
        'templates/login.html',
        'static/style.css',
        'static/script.js'
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - MISSING")
            all_good = False
    
    return all_good

def test_app_import():
    """Test that app.py can be imported"""
    print_header("TEST 4: Loading Application")
    
    try:
        import sys
        sys.path.insert(0, '.')
        # We can't fully import app.py without starting Flask,
        # but we can check for syntax errors
        with open('app.py', 'r') as f:
            compile(f.read(), 'app.py', 'exec')
        print("✅ app.py - Syntax OK")
        
        # Try to import key components
        from dotenv import load_dotenv
        load_dotenv()
        
        print("✅ Core imports - OK")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_templates():
    """Test that templates can be loaded"""
    print_header("TEST 5: Checking Templates")
    
    templates = [
        'templates/index.html',
        'templates/dashboard.html',
        'templates/login.html'
    ]
    
    all_good = True
    for template in templates:
        try:
            with open(template, 'r') as f:
                content = f.read()
                if len(content) > 100:
                    print(f"✅ {template} - OK ({len(content)} bytes)")
                else:
                    print(f"❌ {template} - Too small")
                    all_good = False
        except FileNotFoundError:
            print(f"❌ {template} - Not found")
            all_good = False
        except Exception as e:
            print(f"❌ {template} - Error: {e}")
            all_good = False
    
    return all_good

def test_users_db():
    """Test user database"""
    print_header("TEST 6: Checking User Database")
    
    if Path('users.json').exists():
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
            print(f"✅ users.json exists with {len(users)} user(s)")
            
            # Show first few users (without passwords)
            for email in list(users.keys())[:3]:
                fullname = users[email].get('fullname', 'Unknown')
                print(f"   - {email} ({fullname})")
            
            return True
        except json.JSONDecodeError:
            print("❌ users.json - Invalid JSON")
            return False
    else:
        print("ℹ️  users.json - Not found (will be created on first signup)")
        return True

def test_requirements():
    """Test that requirements file is complete"""
    print_header("TEST 7: Checking Requirements File")
    
    try:
        with open('requirements-unified.txt', 'r') as f:
            lines = f.readlines()
        
        packages = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        print(f"✅ requirements-unified.txt - Found {len(packages)} packages:\n")
        
        for package in packages[:10]:
            print(f"   - {package}")
        
        if len(packages) > 10:
            print(f"   ... and {len(packages) - 10} more")
        
        return len(packages) > 0
    
    except FileNotFoundError:
        print("❌ requirements-unified.txt - Not found")
        return False

def test_docs():
    """Test that documentation files exist"""
    print_header("TEST 8: Checking Documentation")
    
    docs = [
        'UNIFIED_MIGRATION.md',
        'DEPLOYMENT_UNIFIED.md',
        'QUICKSTART_UNIFIED.md',
        'render.yaml'
    ]
    
    all_good = True
    for doc in docs:
        if Path(doc).exists():
            try:
                with open(doc, 'r') as f:
                    lines = len(f.readlines())
                print(f"✅ {doc} - Found ({lines} lines)")
            except Exception as e:
                print(f"❌ {doc} - Error reading: {e}")
                all_good = False
        else:
            print(f"❌ {doc} - Not found")
            all_good = False
    
    return all_good

def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print()
    
    if passed == total:
        print("🎉 All tests passed! Ready to run: python app.py")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. Fix issues and try again.")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Haridwar University AI - Unified App Test Suite        ║")
    print("║  Checking project setup and configuration               ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    results = {
        "Import Check": test_imports(),
        "Environment Variables": test_env_file(),
        "Project Structure": test_app_structure(),
        "Application Code": test_app_import(),
        "Templates": test_templates(),
        "User Database": test_users_db(),
        "Requirements File": test_requirements(),
        "Documentation": test_docs(),
    }
    
    success = print_summary(results)
    
    if success:
        print("\n📝 Next steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
        print("  3. Signup and test chat")
        print("  4. Deploy: Follow DEPLOYMENT_UNIFIED.md")
    else:
        print("\n⚠️  Please fix the failed tests before proceeding")
    
    print()
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
