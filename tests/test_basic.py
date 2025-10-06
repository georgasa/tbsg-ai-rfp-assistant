"""
Basic tests for TBSG AI RFP Assistant
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all main modules can be imported"""
    try:
        from rag_client import TemenosRAGClient
        from word_generator import WordDocumentGenerator
        from shared_config import API_CONFIG
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import modules: {e}")

def test_rag_client_initialization():
    """Test RAG client can be initialized"""
    try:
        from rag_client import TemenosRAGClient
        client = TemenosRAGClient()
        assert client is not None
        assert hasattr(client, 'api_calls_count')
    except Exception as e:
        pytest.fail(f"Failed to initialize RAG client: {e}")

def test_word_generator_initialization():
    """Test Word document generator can be initialized"""
    try:
        from word_generator import WordDocumentGenerator
        generator = WordDocumentGenerator()
        assert generator is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize Word generator: {e}")

def test_shared_config():
    """Test shared configuration is accessible"""
    try:
        from shared_config import API_CONFIG
        assert API_CONFIG is not None
        assert isinstance(API_CONFIG, dict)
    except Exception as e:
        pytest.fail(f"Failed to access shared config: {e}")

def test_basic_functionality():
    """Test basic functionality without external dependencies"""
    # Test that we can create basic objects
    from rag_client import TemenosRAGClient
    from word_generator import WordDocumentGenerator
    
    client = TemenosRAGClient()
    generator = WordDocumentGenerator()
    
    # Test that API calls count is initialized
    assert client.api_calls_count == 0
    
    # Test that objects have expected methods
    assert hasattr(client, 'analyze_pillar')
    assert hasattr(generator, 'create_combined_document')
