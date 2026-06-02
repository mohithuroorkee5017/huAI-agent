"""
Test script for vision API endpoint
"""
import requests
import json
import os
from pathlib import Path

# Configuration
FASTAPI_URL = "http://127.0.0.1:8000"
TEST_IMAGE_PATH = os.path.join(os.path.dirname(__file__), 'test_image.png')

def test_vision_endpoint():
    """Test the /analyze-image endpoint"""
    
    print("=" * 70)
    print("Testing HU Voice AI Vision API")
    print("=" * 70)
    
    # Check test image exists
    if not os.path.exists(TEST_IMAGE_PATH):
        print(f"[ERROR] Test image not found: {TEST_IMAGE_PATH}")
        print("[INFO] Create test image first: python create_test_image.py")
        return
    
    print(f"\n[1] Test Image Path: {TEST_IMAGE_PATH}")
    print(f"[2] File Size: {os.path.getsize(TEST_IMAGE_PATH)} bytes")
    
    # Prepare the request
    endpoint = f"{FASTAPI_URL}/analyze-image"
    print(f"\n[3] Endpoint: POST {endpoint}")
    
    with open(TEST_IMAGE_PATH, 'rb') as img_file:
        files = {'file': img_file}
        data = {'prompt': 'Describe what you see in this image. List all objects.'}
        
        print("[4] Request Headers:")
        print("    - Content-Type: multipart/form-data")
        print("[5] Form Data:")
        print(f"    - file: test_image.png")
        print(f"    - prompt: Describe what you see in this image. List all objects.")
        
        try:
            print("\n[6] Sending request...")
            response = requests.post(endpoint, files=files, data=data, timeout=90)
            
            print(f"[7] Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print("\n✓ SUCCESS - Response JSON:")
                print(json.dumps(result, indent=2))
                
                print("\n[8] Response Details:")
                print(f"    - Success: {result.get('success')}")
                print(f"    - Answer Length: {len(result.get('answer', ''))} chars")
                print(f"    - Objects Count: {len(result.get('objects', []))}")
                print(f"    - Objects: {result.get('objects', [])}")
                print(f"    - Timestamp: {result.get('timestamp')}")
                print(f"    - Image File: {result.get('image_file')}")
                
                print("\n[9] Full Answer:")
                print(result.get('answer', 'N/A'))
                
            else:
                print(f"\n✗ ERROR - Status {response.status_code}")
                print("Response:")
                print(response.text)
                
        except requests.exceptions.Timeout:
            print("[ERROR] Request timeout (vision tasks can take 60+ seconds)")
            print("[INFO] Check FastAPI console for processing status")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Connection failed")
            print("[INFO] Ensure FastAPI is running on port 8000")
            print("[INFO] Run: cd api && python -m uvicorn main:app --host 127.0.0.1 --port 8000")
        except Exception as e:
            print(f"[ERROR] {type(e).__name__}: {str(e)}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    test_vision_endpoint()
