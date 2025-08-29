"""
Setup script for the demo
Creates sample documents and required directories
"""
# import shutil
from pathlib import Path

def setup_demo():
    """Set up the demo environment"""
    demo_dir = Path(__file__).parent
    sample_docs_dir = demo_dir / "sample_docs"
    
    # Create directories
    sample_docs_dir.mkdir(exist_ok=True)
    
    # Create sample text document
    sample_text = """
    Sample Document 3
    
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
    common themes across different document types.
    """
    
    with open(sample_docs_dir / "sample3.txt", "w") as f:
        f.write(sample_text)
    
    print("Demo setup complete. Please add your sample PDFs to the sample_docs directory.")

if __name__ == "__main__":
    setup_demo()
