"""Test configuration and fixtures"""
import pytest
from pathlib import Path
import sys

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture
def test_files():
    """Create test files for document processing"""
    test_dir = Path(__file__).parent / "test_files"
    test_dir.mkdir(exist_ok=True)
    
    # Create a test text file
    text_file = test_dir / "test.txt"
    text_file.write_text("""This is a test document for the chatbot.
    
    This is a sample text document that demonstrates the chatbot's ability to process
    plain text files. It contains multiple paragraphs and discusses various topics
    that can be analyzed for themes.
    
    The chatbot should be able to:
    1. Extract this text
    2. Process it into meaningful chunks
    3. Index it for searching
    4. Use it to answer questions
    5. Identify themes across multiple documents
    
    This sample document can be used alongside PDF files to demonstrate
    the system's ability to work with multiple file formats and find
    common themes across different document types.""")
    
    return {
        "text_file": text_file,
        "dir": test_dir
    }

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Setup test environment variables"""
    monkeypatch.setenv("GEMINI_API_KEY", "test_key")
