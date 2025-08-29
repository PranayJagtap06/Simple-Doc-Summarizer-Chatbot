"""
Demo script for Document Research & Theme Identification Chatbot
This script demonstrates the key features of the chatbot by:
1. Uploading sample documents
2. Asking questions
3. Analyzing themes
"""
import requests
import time
from pathlib import Path
import logging
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
# from rich import print as rprint

# Configure logging and console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

# API Configuration
API_URL = "http://localhost:8080/api/v1"
DEMO_DOCS_PATH = Path(__file__).parent / "sample_docs"


class ChatbotDemo:
    """Demo class to showcase chatbot functionality"""

    def __init__(self):
        self.uploaded_docs = []

    def check_api_health(self) -> bool:
        """Check if the API is running"""
        try:
            response = requests.get(f"{API_URL[:-6]}/health")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def upload_documents(self, doc_paths: List[Path]) -> None:
        """Upload sample documents to the API"""
        files = []
        for path in doc_paths:
            if path.exists():
                files.append(("files", open(path, "rb")))

        try:
            response = requests.post(
                f"{API_URL}/documents/upload",
                files=files,
                params={"files_existing": len(self.uploaded_docs)}
            )
            response.raise_for_status()
            self.uploaded_docs.extend(response.json()["results"])
            console.print(
                f"[green]✓ Uploaded {len(files)} documents successfully[/green]")
        except requests.RequestException as e:
            console.print(f"[red]✗ Error uploading documents: {e}[/red]")
        finally:
            for _, f in files:
                f.close()

    def ask_question(self, query: str) -> Dict[str, Any]:
        """Send a query to the chatbot"""
        try:
            response = requests.post(
                f"{API_URL}/chat/query",
                json={"query": query}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            console.print(f"[red]✗ Error querying chatbot: {e}[/red]")
            return {}

    def display_results(self, results: Dict[str, Any]) -> None:
        """Display the chatbot's response in a formatted way"""
        if not results:
            return

        # Display query
        console.print(Panel(
            f"[bold blue]Q: {results['query']}[/bold blue]",
            title="Question", padding=(1, 2, 1, 2), style="blue"
        ))
        console.print()

        # Display document-specific answers
        if results.get("answers"):
            console.print(Panel(
                "\n".join([
                    f"[bold]{ans['doc_id']}[/bold] ({ans['citation']})\n{ans['answer']}\n"
                    for ans in results["answers"]
                ]),
                title="Document Answers"
            ))

        # Display themes
        if results.get("themes", {}).get("themes"):
            console.print(Panel(
                "\n".join([
                    f"[bold]{theme['name']}[/bold]\n{theme['summary']}\n"
                    for theme in results["themes"]["themes"]
                ]),
                title="Identified Themes"
            ))


def main():
    """Main demo function"""
    demo = ChatbotDemo()

    # Check if API is running
    console.print("[bold]Checking API health...[/bold]")
    if not demo.check_api_health():
        console.print(
            "[red]✗ API is not running. Please start the API first.[/red]")
        return

    console.print("[green]✓ API is running[/green]")

    # Sample documents
    sample_docs = [
        DEMO_DOCS_PATH / "sample1.pdf",
        DEMO_DOCS_PATH / "sample2.png",
        DEMO_DOCS_PATH / "sample3.txt"
    ]

    # Upload documents
    with console.status("[bold]Uploading sample documents..."):
        demo.upload_documents(sample_docs)

    # Sample questions to demonstrate capabilities
    questions = [
        "What are the main themes across all documents?",
        "What are the key findings from these documents?",
        "Summarize the similarities between these documents.",
    ]

    # Process each question
    for question in questions:
        with console.status(f"[bold]Processing question: {question}[/bold]"):
            results = demo.ask_question(question)
            demo.display_results(results)
            time.sleep(2)  # Pause between questions


if __name__ == "__main__":
    console.print(
        "[bold]Document Research & Theme Identification Chatbot Demo[/bold]")
    console.print("=" * 80 + "\n")
    main()
