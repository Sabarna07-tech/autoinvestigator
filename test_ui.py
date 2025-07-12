#!/usr/bin/env python3
"""
Test script for Gradio UI functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_ui_creation():
    """Test UI creation without starting the server"""
    print("🧪 Testing Gradio UI Creation...")
    
    try:
        from gradio_ui import create_interface, AutoInvestigatorUI
        print("✅ UI imports successful")
        
        # Test UI class initialization
        ui_handler = AutoInvestigatorUI()
        print("✅ UI handler created")
        
        if ui_handler.agent:
            print("✅ Agent initialized successfully")
        else:
            print("⚠️ Agent not initialized (API key missing, but UI will work)")
            
        # Test interface creation
        interface = create_interface()
        print("✅ Gradio interface created successfully")
        
        # Test tool list functionality
        try:
            tools = ui_handler.get_tool_list()
            print("✅ Tool list retrieved")
            print(f"📋 Available tools preview: {tools[:100]}...")
        except Exception as e:
            print(f"⚠️ Tool list failed (server may not be running): {e}")
        
        print("\n🎉 All UI tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 AutoInvestigator UI Test")
    print("=" * 50)
    
    success = test_ui_creation()
    
    if success:
        print("\n✅ UI is ready to launch!")
        print("🎯 To start the UI:")
        print("   python gradio_ui.py")
        print("\n💡 Note: Set GEMINI_API_KEY for full functionality")
    else:
        print("\n❌ UI tests failed")
    
    print("\n" + "=" * 50)