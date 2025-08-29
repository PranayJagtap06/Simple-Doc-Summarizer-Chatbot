# AiInternTask/chatbot_theme_identifier/backend/app/services/chat_service.py
"""
AiInternTask/chatbot_theme_identifier/backend/app/services/chat_service.py
This module defines the ChatService class, which handles chat queries and generates themed responses
using Google Generative AI. It processes queries, extracts answers from search results,
identifies themes across documents, and synthesizes a final response.
"""
import google.generativeai as genai
from typing import Dict, Any, List
from datetime import datetime
# import logging
import re
from ..config import Config
from ..models.schemas import ChatResponse, ThemeAnalysis
from .vector_service import VectorService
from app import logger

# Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class ChatService:
    """
    ChatService handles chat queries and generates themed responses using Google Generative AI.
    It processes queries, extracts answers from search results, identifies themes across documents,
    and synthesizes a final response.
    """
    def __init__(self, google_ai_model: str) -> None:
        """
        __init__ initializes the ChatService with the specified Google AI model.
        It configures the Generative AI client and initializes the vector service for document search.

        Parameters
        ----------
        google_ai_model : str
            The name of the Google AI model to be used for generating responses.
        """
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(google_ai_model)
        self.vector_service = VectorService()

    async def process_query(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        process_query processes the user's query and generates a themed response.
        It extracts answers from the search results, identifies themes across the documents,
        and synthesizes a final response that includes the query, answers, themes, and total documents searched.

        Parameters
        ----------
        query : str
            The user's query to be processed.
        search_results : List[Dict[str, Any]]
            The search results containing documents relevant to the query.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the query, timestamp, answers, themes, and total documents searched.
            If an error occurs during processing, it logs the error and raises an exception.
        """
        try:
            # Extract answers from documents
            answers = await self._extract_answers(query, search_results)

            # Identify themes
            themes = await self._identify_themes(query, answers)
            logger.info("Chat query processed successfully")

            return ChatResponse(
                query=query,
                timestamp=datetime.now(),
                answers=answers,
                themes=themes,
                total_docs_searched=len(
                    {r["metadata"]["doc_id"] for r in search_results})
            ).model_dump()

        except Exception as e:
            logger.error(f"Error synthesizing response: {e}")
            raise

    async def _extract_answers(self, query: str, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        _extract_answers extracts answers from the search results based on the user's query.
        It processes each document, generates a prompt for the AI model, and retrieves concise answers.
        It ensures that each document is processed only once to avoid redundancy.

        Parameters
        ----------
        query : str
            The user's query to be answered based on the document content.
        search_results : List[Dict[str, Any]]
            The search results containing documents relevant to the query.

        Returns
        -------
        List[Dict[str, Any]]
            A list of dictionaries containing answers extracted from the documents.
            Each dictionary includes the document ID, filename, answer text, citation, page, and paragraph.
            If no relevant information is found in a document, it skips that document.
        """
        answers = []
        processed_docs = set()

        for result in search_results:
            doc_id = result["metadata"]["doc_id"]
            if doc_id in processed_docs:
                continue

            processed_docs.add(doc_id)
            doc_chunks = [
                r for r in search_results if r["metadata"]["doc_id"] == doc_id]
            doc_text = "\n".join([chunk["text"] for chunk in doc_chunks[:3]])

            try:
                prompt = f'''
                Based on this document content, answer: "{query}"

                Content: {doc_text}

                Instructions:
                1. Provide a direct, specific answer if the information is available
                2. If no relevant information is found, respond with "No relevant information found"
                3. Keep the answer concise and factual
                4. Focus on the most relevant information
                
                Answer:
                '''

                response = self.model.generate_content(prompt)
                answer_text = response.text.strip()

                if answer_text and "no relevant information" not in answer_text.lower():
                    best_chunk = doc_chunks[0]
                    answers.append({
                        "doc_id": doc_id,
                        "filename": result["metadata"]["filename"],
                        "answer": answer_text,
                        "citation": f"Page {best_chunk['metadata']['page']}, Para {best_chunk['metadata']['paragraph']}",
                        "page": best_chunk["metadata"]["page"],
                        "paragraph": best_chunk["metadata"]["paragraph"]
                    })
                logger.info(f'Successfully extracted answers from {doc_id}')

            except Exception as e:
                logger.error(f"Error extracting answer from {doc_id}: {e}")
                continue


        return answers

    async def _identify_themes(self, query: str, answers: List[Dict[str, Any]]) -> ThemeAnalysis:
        """
        _identify_themes identifies themes across the answers extracted from the documents.
        It analyzes the answers to find common themes, summarizes them, and provides an overall synthesis.

        Parameters
        ----------
        query : str
            The user's query for which themes are being identified.
        answers : List[Dict[str, Any]]
            The list of answers extracted from the documents relevant to the query.

        Returns
        -------
        ThemeAnalysis
            An object containing identified themes and an overall synthesis.
            If no relevant information is found, it returns a default theme analysis indicating that.
        """
        if not answers:
            return ThemeAnalysis(themes=[], synthesis="No relevant information found.")

        try:
            answers_text = "\n".join([
                f"Document {ans['doc_id']}: {ans['answer']}"
                for ans in answers
            ])

            prompt = f'''
            Analyze these document answers for the query: "{query}"
            
            Answers:
            {answers_text}
            
            Instructions:
            1. Identify 2-4 main themes that emerge across these documents
            2. For each theme, provide:
               - A clear theme name
               - A summary of what documents support this theme
               - The specific document IDs that relate to this theme
            3. Provide an overall synthesis that combines insights from all themes
            4. Ensure themes are distinct and meaningful
            
            Format as:
            THEME [Serial Number]: [Name]
            Documents: [Doc IDs]
            Summary: [Description]

            OVERALL SYNTHESIS:
            [Combined insights and conclusions]
            '''

            response = self.model.generate_content(prompt)
            themes = self._parse_themes(response.text, answers)
            logger.info('Successfully identified themes for chat query')
            return themes

        except Exception as e:
            logger.error(f"Error identifying themes: {e}")
            return ThemeAnalysis(
                themes=[{
                    "name": "General Analysis",
                    "summary": "Error analyzing themes",
                    "supporting_documents": []
                }],
                synthesis="Error analyzing themes across documents."
            )

    def _parse_themes(self, response_text: str, answers: List[Dict[str, Any]]) -> ThemeAnalysis:
        """
        _parse_themes parses the response text from the AI model to extract themes and their summaries.
        It identifies individual themes, their supporting documents, and provides an overall synthesis.

        Parameters
        ----------
        response_text : str
            The text response generated by the AI model containing themes and summaries.
        answers : List[Dict[str, Any]]
            The list of answers extracted from the documents relevant to the query.

        Returns
        -------
        ThemeAnalysis
            An object containing identified themes and an overall synthesis.
            If parsing fails, it returns a default theme analysis with a general analysis.
        """
        themes = []
        synthesis = ""

        try:
            sections = response_text.split("OVERALL SYNTHESIS:")
            # if len(sections) == 2:
            theme_section = sections[0]
            synthesis = sections[1].strip()
            # else:
            # theme_section = response_text
            # synthesis = "Multiple themes identified across the documents."

            # Extract individual themes
            theme_matches = re.findall(
                r"THEME \d+: (.+?)\nDocuments: (.+?)\nSummary: (.+?)(?=\nTHEME|\n\nOVERALL|\Z)",
                theme_section,
                re.DOTALL,
            )

            for match in theme_matches:
                theme_name, doc_refs, summary = match

                # Extract document IDs mentioned in the theme
                mentioned_docs = re.findall(r"DOC\w+", doc_refs)
                supporting_docs = [
                    ans
                    for ans in answers
                    if ans["doc_id"] in mentioned_docs
                    or any(doc_id in doc_refs for doc_id in [ans["doc_id"]])
                ]

                themes.append(
                    {
                        "name": theme_name.strip(),
                        "summary": summary.strip(),
                        "supporting_documents": supporting_docs,
                        "document_count": len(supporting_docs),
                    }
                )

            logger.info('Parsed themes successfully')
            # return {"themes": themes, "synthesis": synthesis}

        except Exception as e:
            logger.error(f"Error parsing theme response: {e}")
            themes = [
                {
                    "name": "General Analysis",
                    "summary": response_text,
                    "supporting_documents": answers,
                    "document_count": len(answers),
                }
            ]
            synthesis = response_text.strip()

        return ThemeAnalysis(
            themes=themes,
            synthesis=synthesis
        )
