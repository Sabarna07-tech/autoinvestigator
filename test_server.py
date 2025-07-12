#!/usr/bin/env python3
"""
Demo script to test AutoInvestigator server functionality
This tests the basic server endpoints without requiring Gemini API key
"""

import requests
import json
import uuid
from client.config import SERVER_URL

def test_server_connection():
    """Test basic server connectivity"""
    print(f"🔗 Testing server connection to: {SERVER_URL}")
    try:
        # Test tool list endpoint
        payload = {
            "id": f"test-{uuid.uuid4()}",
            "requests": [
                {
                    "id": f"tools-list-{uuid.uuid4()}",
                    "method": "tools/list"
                }
            ]
        }
        
        response = requests.post(SERVER_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Server is responding")
            print("📋 Available tools:")
            if 'results' in result and result['results']:
                tools = result['results'][0].get('results', ['No tools found'])
                for tool in tools:
                    print(f"   {tool}")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the server running?")
        print(f"   Try starting the server with: python server.py")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality that doesn't require API keys"""
    print("\n🧪 Testing basic server functionality...")
    
    try:
        # Test prompt endpoints
        payload = {
            "id": f"test-prompts-{uuid.uuid4()}",
            "requests": [
                {
                    "id": f"prompt-list-{uuid.uuid4()}",
                    "method": "prompt/list"
                },
                {
                    "id": f"prompt-template-{uuid.uuid4()}",
                    "method": "prompt/request_template"
                }
            ]
        }
        
        response = requests.post(SERVER_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prompt endpoints working")
            
            # Display prompt list
            if len(result['results']) > 0:
                prompts = result['results'][0].get('results', [])
                print(f"📝 Available prompts: {prompts}")
                
            # Display request template
            if len(result['results']) > 1:
                template = result['results'][1].get('results', ['No template'])
                print("📋 Request template available")
                
            return True
        else:
            print(f"❌ Prompt test failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing basic functionality: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AutoInvestigator Server Test")
    print("=" * 50)
    
    # Test server connection
    server_ok = test_server_connection()
    
    if server_ok:
        # Test basic functionality
        basic_ok = test_basic_functionality()
        
        if basic_ok:
            print("\n✅ Server tests passed!")
            print("🎯 You can now start the Gradio UI with: python gradio_ui.py")
        else:
            print("\n⚠️ Basic functionality tests failed")
    else:
        print("\n❌ Server connection failed")
        print("💡 Make sure to start the server first:")
        print("   python server.py")
    
    print("\n" + "=" * 50)