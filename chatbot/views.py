import os
import re
from django.conf import settings
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from decouple import config

from .models import Document, ChatSession, ChatMessage
from .serializers import (
    DocumentSerializer,
    ChatSessionSerializer,
    ChatSessionDetailSerializer,
    ChatMessageSerializer,
    ChatQuerySerializer,
    ChatResponseSerializer
)

try:
    import anthropic
    from PyPDF2 import PdfReader
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False


# ==================== Helper Functions ====================

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyPDF2"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {file_path}: {str(e)}")
        return ""


def get_all_knowledge_base_documents():
    """
    Scan both Document model AND Publication model for PDFs.
    Returns unified list of document dictionaries.
    """
    documents = []

    # 1. Get Documents from chatbot.Document model
    chatbot_docs = Document.objects.filter(is_active=True)
    for doc in chatbot_docs:
        if doc.file and doc.file.name.lower().endswith('.pdf'):
            documents.append({
                'id': doc.id,
                'name': doc.name,
                'path': doc.file.path,
                'url': doc.file_url,
                'type': 'document',
                'description': doc.description or ''
            })

    # 2. Get Publications from resources.Publication model
    try:
        from resources.models import Publication
        publications = Publication.objects.all()
        for pub in publications:
            if pub.pdf:  # Has PDF file
                # Construct full URL using FULL_MEDIA_URL to point to backend
                if hasattr(settings, 'FULL_MEDIA_URL'):
                    pdf_url = settings.FULL_MEDIA_URL.rstrip('/') + '/' + str(pub.pdf)
                else:
                    pdf_url = settings.MEDIA_URL + str(pub.pdf)
                
                documents.append({
                    'id': pub.id,
                    'name': pub.title,
                    'path': pub.pdf.path,
                    'url': pdf_url,
                    'type': 'publication',
                    'description': pub.description
                })
            elif pub.url:  # Has external URL
                documents.append({
                    'id': pub.id,
                    'name': pub.title,
                    'path': None,
                    'url': pub.url,
                    'type': 'publication',
                    'description': pub.description
                })
    except ImportError:
        # resources app not available, skip publications
        pass
    except Exception as e:
        print(f"Error loading publications: {str(e)}")

    return documents


def build_conversation_context(session_id):
    """
    Build conversation history for Claude context.
    Returns formatted string of last 5 message pairs.
    """
    if not session_id:
        return ""

    try:
        session = ChatSession.objects.get(id=session_id)
        # Get last 10 messages (5 pairs of user/assistant)
        recent_messages = session.messages.all().order_by('-created_at')[:10]

        if not recent_messages:
            return ""

        context = "\n\nPrevious conversation:\n"
        for msg in reversed(recent_messages):
            role = "User" if msg.message_type == "user" else "Assistant"
            context += f"{role}: {msg.content}\n"

        return context
    except ChatSession.DoesNotExist:
        return ""


def find_relevant_document(query, documents, conversation_context="", client=None):
    """
    Stage 1: Use Claude Haiku to select most relevant document.
    Returns index of selected document.
    """
    if not client or not documents:
        return 0

    # Prepare document summaries
    doc_summaries = "\n\n".join([
        f"Document {i+1}: {doc['name']} ({doc['type']})\n"
        f"Description: {doc.get('description', 'N/A')}\n"
        f"Preview: {doc.get('preview', '')[:500]}..."
        for i, doc in enumerate(documents)
    ])

    prompt = f"""You are a document search assistant for CEPA (Centre for Parliamentary Accountability).
    Given a user question and a list of documents, identify which document is most relevant.
    
    {conversation_context}
    
    User Question: {query}
    
    Available Documents:
    {doc_summaries}
    
    Respond with ONLY the document number (1, 2, 3, etc.) that is most relevant to the question.
    If no document is relevant, respond with "1"."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )

        selected_doc_num = response.content[0].text.strip()

        # Parse document number
        try:
            doc_index = int(re.search(r'\d+', selected_doc_num).group()) - 1
            if doc_index < 0 or doc_index >= len(documents):
                doc_index = 0  # Default to first document
        except:
            doc_index = 0

        return doc_index
    except Exception as e:
        print(f"Error in find_relevant_document: {str(e)}")
        return 0


def generate_answer(query, selected_doc, conversation_context="", client=None):
    """
    Stage 2: Use Claude Haiku to generate answer from selected document.
    Returns answer text.
    """
    if not client:
        return "Error: Claude API client not initialized."

    prompt = f"""You are a helpful assistant answering questions about CEPA (Centre for Parliamentary Accountability) and parliamentary proceedings in Uganda.

    {conversation_context}
    
    User Question: {query}
    
    Document Name: {selected_doc['name']}
    Document Type: {selected_doc['type']}
    
    Document Content:
    {selected_doc.get('full_text', '')[:50000]}
    
    Please provide a clear, concise answer to the user's question based on the document content.
    If the answer is not in the document, say so clearly. Keep your answer under 300 words."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()
    except Exception as e:
        return f"Error generating answer: {str(e)}"


# ==================== ViewSets ====================

class DocumentViewSet(viewsets.ModelViewSet):
    """Standard CRUD for Documents"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active documents"""
        active_docs = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_docs, many=True)
        return Response(serializer.data)


class ChatSessionViewSet(viewsets.ModelViewSet):
    """Session management"""
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    pagination_class = PageNumberPagination
    ordering = ['-last_activity']

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return ChatSessionDetailSerializer
        return ChatSessionSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active sessions"""
        active_sessions = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_sessions, many=True)
        return Response(serializer.data)


class ChatViewSet(viewsets.ViewSet):
    """Main chatbot logic"""

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        Process a chat query and return AI response.
        Creates or continues a session.
        """
        # Check dependencies
        if not HAS_DEPENDENCIES:
            return Response(
                {'error': 'Required dependencies not installed. Please install: anthropic, PyPDF2'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Validate request
        serializer = ChatQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data['query']
        session_id = serializer.validated_data.get('session_id')

        # Get or create session
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                return Response(
                    {'error': 'Session not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Create new session with title from query preview
            session_title = query[:50] + "..." if len(query) > 50 else query
            session = ChatSession.objects.create(session_title=session_title)

        # Get Claude API key
        claude_api_key = config('CLAUDE_API_KEY', default=None)
        if not claude_api_key:
            return Response(
                {'error': 'Claude API key not configured. Please set CLAUDE_API_KEY in environment variables.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Initialize Claude client
            client = anthropic.Anthropic(api_key=claude_api_key)

            # Get all documents from both sources
            documents = get_all_knowledge_base_documents()
            if not documents:
                return Response(
                    {'error': 'No documents found in knowledge base'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extract text from all documents
            document_contents = []
            for doc in documents:
                text = extract_text_from_pdf(doc['path'])
                if text:
                    # Take first 10000 characters for relevance check
                    preview = text[:10000]
                    document_contents.append({
                        **doc,
                        'preview': preview,
                        'full_text': text
                    })

            if not document_contents:
                return Response(
                    {'error': 'No readable text found in documents'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Build conversation context
            conversation_context = build_conversation_context(session.id)

            # Stage 1: Find relevant document
            doc_index = find_relevant_document(
                query, document_contents, conversation_context, client
            )
            selected_doc = document_contents[doc_index]

            # Stage 2: Generate answer
            answer = generate_answer(
                query, selected_doc, conversation_context, client
            )

            # Create user message
            user_message = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=query
            )

            # Create assistant message
            assistant_message = ChatMessage.objects.create(
                session=session,
                message_type='assistant',
                content=answer,
                source_document_name=selected_doc['name'],
                source_document_url=selected_doc['url'],
                source_document_type=selected_doc['type'],
                confidence=0.8
            )

            # Build response
            response_data = {
                'session_id': session.id,
                'user_message_id': user_message.id,
                'assistant_message_id': assistant_message.id,
                'answer': answer,
                'source_document_name': selected_doc['name'],
                'source_document_url': selected_doc['url'],
                'source_document_type': selected_doc['type'],
                'confidence': 0.8,
                'timestamp': assistant_message.created_at
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Error processing request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
