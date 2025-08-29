"""Tests for the Streamlit interface"""
import pytest
from streamlit.testing.v1 import AppTest
import sys
from pathlib import Path

ST_APP_PATH = str(Path(__file__).parent.parent / "backend" / "app.py")  # Update path to match your app location

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

def test_streamlit_initial_state():
    """Test initial state of Streamlit app"""
    at = AppTest.from_file(ST_APP_PATH)  # Update path to match your app location
    at.run(timeout=10)
    
    # Test page title and initial state
    assert len(at.title) > 0
    assert "Document Research & Theme Identification Chatbot" in at.title[0].value

def test_streamlit_file_upload(test_files):
    """Test file upload functionality"""
    at = AppTest.from_file(ST_APP_PATH)
    # Simulate file upload by setting session state
    at.session_state["uploaded_files"] = [str(test_files["text_file"])]
    at.run(timeout=10)
    # Now check if the process button appears
    buttons = at.get("button")
    print(buttons)
    assert buttons is not None and len(buttons) > 0

def test_streamlit_chat_query(test_files):
    """Test chat query functionality"""
    at = AppTest.from_file(ST_APP_PATH)
    # Simulate file upload and processing
    at.session_state["uploaded_files"] = [str(test_files["text_file"])]
    at.session_state["processed"] = True  # If your app uses a flag for processed files
    at.run(timeout=10)
    # Now the text_input should be available
    text_inputs = at.get("text_input")
    assert text_inputs is not None and len(text_inputs) > 0
    query_input = text_inputs[0]
    query_input.set_value("What is this document about?")
    # Find and test search button
    buttons = at.get("button")
    print(buttons)
    assert buttons is not None and len(buttons) > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
