# chatbot_theme_identifier/app.py
"""
This code is part of a Streamlit application that allows users to upload documents, query them, and identify themes within the content.
"""
import base64
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import requests
import streamlit as st

# import logging
from app import logger
from icecream import ic

# Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

about: str = """# Doc Theme Identification Chatbot\n*Doc Theme Identification Chatbot* is a *Google Gemini AI* based AI chatbot. It can extract answers and generate appropriate themes from the uploaded documents based on user query."""

# Page configuration
st.set_page_config(
    page_title="Document Research & Theme Identification Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": about}
)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# API Configuration
import os
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")


def post_request(url: str, files: Optional[List[Any]]=None, params: Optional[Dict[str, Any]]=None, json: Optional[Dict[str, Any]]=None) -> Optional[requests.Response]:
    """
    post_request sends a POST request to the specified URL with the provided data.
    It handles the response and returns the JSON content if successful.
    If an error occurs, it logs the error and returns an empty dictionary.

    Parameters
    ----------
    url : str
        The URL to which the POST request is sent.
    data : Dict[str, Any]
        The data to be sent in the POST request.

    Returns
    -------
    Dict[str, Any]
        Returns the JSON response from the server or an empty dictionary on error.
    """
    try:
        response = requests.post(url, files=files, params=params, json=json)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in post_request: {str(e)}")
        st.error(f"Error uploading files: {str(e)}")
        return None


def upload_files(files: Optional[List[Any]], files_exists: int = 0) -> List[Dict[str, Any]]:
    """
    upload_files Initializes the upload of files to the backend API.
    This function sends a POST request to the backend API to upload the provided files.
    It handles the response and returns a list of dictionaries containing the results of the upload.
    It also handles errors and logs them appropriately.

    Parameters
    ----------
    files : Optional[List[Any]]
        List of files to be uploaded. Each file should be a file-like object.
    files_exists : int, optional
        Number of pre-existing files in streamlit session, by default 0

    Returns
    -------
    List[Dict[str, Any]]
        Returns a list of dictionaries containing processed documents content.
    If no files are provided, it returns an empty list.
    """
    if not files:
        return []

    try:
        files_data = [("files", file) for file in files]
        # response = requests.post(
        #     f"{API_URL}/documents/upload", files=files_data, params={"files_existing": files_exists})
        # response.raise_for_status()
        response = post_request(
            url=f"{API_URL}/documents/upload",
            files=files_data, params={"files_existing": files_exists})
        # ic(type(response.json()['results']), len(response.json()['results']), response.json()['results'][0].keys())
        if response is None:
            logger.error("No response received from the server.")
            st.error("No response received from the server.")
            return []
        if not response.ok:
            logger.error(f"Failed to upload files: {response.status_code} - {response.text}")
            st.error(f"Failed to upload files: {response.status_code} - {response.text}")
            return []
        # Log the successful upload
        logger.info(
            f"Uploaded {len(response.json()['results'])} files successfully.")
        st.success(
            f"Uploaded {len(response.json()['results'])} files successfully.")
        return response.json()["results"]

    except requests.exceptions.RequestException as e:
        # Log the error
        logger.error(f"Error uploading files: {str(e)}")
        st.error(f"Error uploading files: {str(e)}")
        return []


def query_documents(question: str) -> Optional[Dict[str, Any]]:
    """
    query_documents sends a query to the backend API to retrieve answers from uploaded documents.
    This function sends a POST request to the backend API with the user's question.
    It handles the response and returns a dictionary containing the query results.
    It also handles errors and logs them appropriately.

    Parameters
    ----------
    question : str
        The question to be asked about the uploaded documents.
        If the question is empty, it returns None.

    Returns
    -------
    Optional[Dict[str, Any]]
        Returns a dictionary containing the query results, including answers and themes.
    """
    try:
        # response = requests.post(
        #     f"{API_URL}/chat/query",
        #     json={"query": question}
        # )
        # response.raise_for_status()
        response = post_request(url=f"{API_URL}/chat/query", json={"query": question})
        # ic(response.json())
        if response is None:
            logger.error("No response received from the server.")
            st.error("No response received from the server.")
            return None
        if not response.ok:
            logger.error(f"Failed to query documents: {response.status_code} - {response.text}")
            st.error(f"Failed to query documents: {response.status_code} - {response.text}")
            return None
        # Log the successful query response
        logger.info(f"\nQuery response: {response.json()}")
        st.success("\nQuery response generated successfully.")
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying documents: {str(e)}")
        st.error(f"Error querying documents: {str(e)}")
        return None


def display_results(results: Dict[str, Any]) -> None:
    """
    display_results displays the results of the document query in the Streamlit app.
    This function formats and displays the answers and themes identified from the documents.

    Parameters
    ----------
    results : Dict[str, Any]
        A dictionary containing the results of the document query.
        It should include keys like "answers" and "themes".
        If there are no results, it simply returns without displaying anything.
        If there are no answers or themes, it displays an appropriate message.

    Returns
    -------
    None
    """
    if not results:
        return

    # Display answers table
    if results.get("answers"):
        st.subheader("📄 Individual Document Answers")
        df = pd.DataFrame([
            {
                "Document ID": ans["doc_id"],
                "File Name": ans["filename"],
                "Answer": ans["answer"][:105] + "..." if len(ans["answer"]) > 105 else ans["answer"],
                "Citation": ans["citation"]
            }
            for ans in results["answers"]
        ])

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Answer": st.column_config.TextColumn(
                    "Answer",
                    help="Double-click to view full answer",
                    max_chars=105
                )
            }
        )

    # Display themes
    if results.get("themes", {}).get("themes"):
        st.subheader("🎯 Synthesized Theme Answer")
        for i, theme in enumerate(results["themes"]["themes"], 1):
            st.markdown(f"**Theme {i} - {theme['name']}**")
            if theme.get("supporting_documents"):
                docs = [
                    f"{doc['doc_id']}" for doc in theme["supporting_documents"]]
                st.markdown(f" {', '.join(docs)}: {theme['summary']}")
            # st.markdown(theme["summary"])
            st.markdown("---")
    else:
        st.info("No specific themes identified for this query.")


def render_sidebar():
    # Sidebar
    with st.sidebar:
        st.title("📁 Document Upload")
        files = st.file_uploader(
            "Upload your documents",
            type=["pdf", "txt", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Supported formats: PDF, TXT, PNG, JPG"
        )

        if files and st.button("Process Documents", type="primary"):
            np.random.seed(42)  # For reproducibility
            with st.spinner("Processing documents..."):
                ic(len(st.session_state.documents))
                # Get list of existing filenames
                existing_filenames = [doc['filename']
                                      for doc in st.session_state.documents]

                # Filter only new files
                new_docs = [
                    file for file in files if file.name not in existing_filenames]

                # ic(new_docs)
                if not new_docs:
                    st.warning("No new documents to process.")
                else:
                    # Upload files to backend
                    results = upload_files(
                        new_docs, files_exists=len(st.session_state.documents))
                    # ic(results)
                    # ic(type(results[0]), len(results[0]), results[0].keys())
                    if results:
                        st.success(f"Processed {len(new_docs)} new documents.")
                        st.session_state.documents.extend(results)
                        # st.rerun()

        get_prf_image('pranay_blusq.jpg')


@st.fragment
def render_document_viewer():
    """Render document viewer tab"""
    st.subheader("📁 Document Library")

    if not st.session_state.documents:
        st.info("No documents uploaded yet.")
        return

    # Filter options
    col1, col2 = st.columns(2)

    with col1:
        doc_types = list(set([doc["type"]
                        for doc in st.session_state.documents]))
        selected_type = st.selectbox("Filter by type", ["All"] + doc_types)

    with col2:
        sort_by = st.selectbox("Sort by", ["Upload Time", "Filename", "Size"])

    # Filter and sort documents
    filtered_docs = st.session_state.documents
    if selected_type != "All":
        filtered_docs = [
            doc for doc in filtered_docs if doc["type"] == selected_type
        ]

    if sort_by == "Upload Time":
        filtered_docs = sorted(
            filtered_docs, key=lambda x: x["upload_time"], reverse=True
        )
    elif sort_by == "Filename":
        filtered_docs = sorted(filtered_docs, key=lambda x: x["filename"])
    elif sort_by == "Size":
        filtered_docs = sorted(
            filtered_docs, key=lambda x: x["size"], reverse=True)

    # Display documents
    for doc in filtered_docs:
        with st.expander(f"{doc['filename']} ({doc['id']})"):
            col_a, col_b = st.columns(2)

            with col_a:
                st.write(f"**Type:** {doc['type']}")
                st.write(f"**Size:** {doc['size']} bytes")
                st.write(f"**Uploaded:** {doc['upload_time']}")

            with col_b:
                st.write(f"**Paragraphs:** {len(doc['paragraphs'])}")
                st.write(f"**Text Length:** {len(doc['text'])} characters")

            # Show text preview and delete button
            col_c, col_d = st.columns(2)
            with col_c:
                try:
                    if st.button("Delete Document", key=f"delete_{doc['filename']}_{doc['id']}"):
                        st.session_state.documents.remove(doc)
                        response = post_request(url=f"{API_URL}/vector/delete-doc/{doc['id']}")
                        if response is None:
                            logger.error("No response received from the server.")
                            st.error("No response received from the server.")
                            return
                        if not response.ok:
                            logger.error(f"Failed to delete document: {response.status_code} - {response.text}")
                            st.error(f"Failed to delete document: {response.status_code} - {response.text}")
                            return
                        st.rerun(scope='fragment')
                        logger.info(f"Document '{doc['filename']}' deleted successfully.")
                        st.success(f"Document '{doc['filename']}' deleted successfully.")
                except ValueError as ve:
                    logger.error(f"Document '{doc['filename']}' not found in session state: {ve}")
                    st.error(f"Document '{doc['filename']}' not found in session state: {ve}")
            with col_d:
                if st.button("Show Preview", key=f"preview_{doc['filename']}_{doc['id']}"):
                    st.text_area(
                        "Document Content",
                        doc["text"][:6000] + "..."
                        if len(doc["text"]) > 6000
                        else doc["text"],
                        height=200,
                    )


def render_main_content():
    st.title("🤖 Document Research & Theme Identification Chatbot")

    # Main content
    if not st.session_state.documents:
        st.info("👋 Upload some documents to get started!")
    else:
        query = st.text_input(
            "Ask a question about your documents:",
            placeholder="e.g., What are the main themes discussed?"
        )

        search_btn = st.button("Search", type="primary")

        if query and search_btn:
            # Store query in session state
            with st.spinner("Analyzing documents..."):
                results = query_documents(query)
                if results:
                    display_results(results)
                    st.session_state.chat_history.append(results)

        # Show chat history
        if st.session_state.chat_history:
            st.subheader("💬 Previous Queries")
            for result in reversed(st.session_state.chat_history):
                with st.expander(f"Query: {result['query']}..."):
                    display_results(result)


def get_prf_image(image_path):
    """Read image file."""
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    
        # Create the HTML for the circular image
        st.markdown(
            """
            ------
            <style>
                a.author {
                    text-decoration: none;
                    color: #F14848;
                }
                a.author:hover {
                    text-decoration: none;
                    color: #14a3ee;
                }
            </style>
            <p><em>Created with</em> ❤️ <em>by <a class='author' href='https://pranayjagtap.netlify.app' rel=noopener noreferrer' target='_blank'><b>Pranay Jagtap</b></a></em></p>
            """,
            unsafe_allow_html=True
        )
        html_code = """
        <style>
            .circular-image {
                width: 125px;
                height: 125px;
                border-radius: 55%;
                overflow: hidden;
                display: inline-block;
            }
            .circular-image img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .author-headline {
                color: #14a3ee
            }
        </style>
        """ + f"""
        <div class="circular-image">
            <img src="data:image/jpeg;base64,{img_base64}" alt="Pranay Jagtap">
        </div>
        <p class=author-headline><b>Machine Learning Enthusiast | Electrical Engineer<br>📍Nagpur, Maharashtra, India<b></p>
        """

        # Display the circular image
        st.markdown(html_code, unsafe_allow_html=True)


def main():
    """
    main function initializes the Streamlit app and handles the main logic.
    """
    render_sidebar()

    # Main content tabs
    tab1, tab2 = st.tabs(["🤖 Chatbot", "📁 Document Library"])

    with tab1:
        render_main_content()

    with tab2:
        render_document_viewer()

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p><b>Disclaimer: Theme identification and description made by the model can be marginally inaccurate. User discretion and expert consultaion is advised. Additionally, we reserve the right to modify or remove AI service.</b><br>So be patient and have a coffee, as it may take some time... Well, it may not take that long, still it's always good to have a ☕...</p>
            <p><em>Document Research & Theme Identification Chatbot</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # get_prf_image('pranay_blusq.jpg')


if __name__ == "__main__":
    main()
