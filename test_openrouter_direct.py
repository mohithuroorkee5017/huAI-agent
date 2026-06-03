#!/usr/bin/env python3
"""
Direct test of OpenRouter API connectivity
"""

import sys
import requests
sys.path.insert(0, 'api')
from config import settings

print('='*70)
print('DIRECT OPENROUTER API TEST')
print('='*70)

print('\n1. Configuration Check:')
print(f'   API Key loaded: {bool(settings.OPENROUTER_API_KEY)}')
if settings.OPENROUTER_API_KEY:
    print(f'   API Key: {settings.OPENROUTER_API_KEY}')
    print(f'   Key Format: {settings.OPENROUTER_API_KEY[:20]}...{settings.OPENROUTER_API_KEY[-4:]}')
else:
    print('   ERROR: API Key not loaded!')
    sys.exit(1)

print('\n2. Header Construction:')
headers = {
    'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}',
    'Content-Type': 'application/json',
    'HTTP-Referer': 'https://huvoiceai.example.com',
    'X-Title': 'HU Voice AI'
}

for key, value in headers.items():
    if key == 'Authorization':
        print(f'   {key}: {value[:30]}...')
    else:
        print(f'   {key}: {value}')

print('\n3. Testing API Request:')
payload = {
    'model': 'openai/gpt-4o-mini',
    'messages': [
        {'role': 'user', 'content': 'Say OK'}
    ],
    'max_tokens': 50
}

try:
    print('   Sending request to https://openrouter.ai/api/v1/chat/completions...')
    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f'\n4. Response:')
    print(f'   Status Code: {response.status_code}')
    print(f'   Headers Sent: {response.request.headers}')
    
    if response.status_code == 200:
        print('   ✓ SUCCESS: API is working!')
        data = response.json()
        if 'choices' in data:
            print(f'   Response: {data["choices"][0]["message"]["content"]}')
    else:
        print(f'   ✗ ERROR: {response.status_code}')
        print(f'   Response: {response.text[:500]}')
        
except Exception as e:
    print(f'   ✗ ERROR: {type(e).__name__}: {e}')

print('\n' + '='*70)
