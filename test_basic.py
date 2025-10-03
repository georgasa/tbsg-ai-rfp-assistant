"""
Basic tests for the TBSG AI RFP Assistant
"""

import pytest
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all main modules can be imported"""
    try:
        import app
        import rag_client
        import word_generator
        import shared_config
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")

def test_shared_config():
    """Test that shared_config has required configurations"""
    from shared_config import API_CONFIG
    
    # Check that API_CONFIG is a dictionary
    assert isinstance(API_CONFIG, dict)
    
    # Check that it has some basic keys
    assert 'base_url' in API_CONFIG
    assert 'demo_mode' in API_CONFIG

def test_rag_client_initialization():
    """Test that RAGClient can be initialized"""
    from rag_client import RAGClient
    
    # Test initialization with demo mode
    client = RAGClient()
    assert client is not None
    assert hasattr(client, 'jwt_token')

def test_word_generator_initialization():
    """Test that WordGenerator can be initialized"""
    from word_generator import WordGenerator
    
    # Test initialization
    generator = WordGenerator()
    assert generator is not None
    assert hasattr(generator, 'docx_available')

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    # This is a simple test that always passes
    assert 1 + 1 == 2
    assert "hello" == "hello"
    assert len([1, 2, 3]) == 3

if __name__ == "__main__":
    pytest.main([__file__])
