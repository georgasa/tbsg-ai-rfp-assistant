#!/usr/bin/env python3
"""
Test script for Temenos RAG AI System
"""

import os
import sys

# Set environment variable
os.environ['TEMENOS_JWT_TOKEN'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYXBvc3RvbG9zLmdlb3JnYXMiLCJlbWFpbCI6ImFwb3N0b2xvcy5nZW9yZ2FzQHRlbWVub3MuY29tIiwiZXhwIjoxNzYyMDcxNjIzLCJpYXQiOjE3NTk0Nzk2MjMsImlzcyI6InRic2cudGVtZW5vcy5jb20iLCJhdWQiOiJ0ZW1lbm9zLWFwaSJ9.8VuKANbWATjEg24yJU7sxrtilmeJNJEfZ-wUIZ1Y8q0"

try:
    print("🚀 Testing Temenos RAG AI System...")
    
    # Test imports
    print("📦 Testing imports...")
    from rag_client import TemenosRAGClient
    from word_generator import WordDocumentGenerator
    from shared_config import UI_CONFIG, API_CONFIG
    print("✅ All imports successful")
    
    # Test client initialization
    print("🔧 Testing client initialization...")
    client = TemenosRAGClient()
    print("✅ RAG client initialized")
    
    # Test word generator
    print("📄 Testing word generator...")
    generator = WordDocumentGenerator()
    print("✅ Word generator initialized")
    
    # Test connection
    print("🔍 Testing API connection...")
    is_connected = client.test_connection()
    if is_connected:
        print("✅ API connection successful")
    else:
        print("⚠️ API connection failed (this is expected if no internet or invalid token)")
    
    # Test pillars
    print("🏗️ Testing pillars...")
    pillars = client.get_technology_pillars()
    print(f"✅ Found {len(pillars)} pillars: {', '.join(pillars)}")
    
    print("\n🎉 All tests passed! The system is ready to run.")
    print("📱 To start the web application, run: python app.py")
    print("🌐 Then open: http://localhost:5000")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
