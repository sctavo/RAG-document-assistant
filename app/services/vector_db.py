import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

def process_and_store_pdf(file_path: str):
    """
    Procesa un archivo PDF: carga, divide, embedde y guarda en ChromaDB.
    """
    try:
        # 1. Cargar el PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # 2. Dividir el texto en chunks (fragmentos)
        # Chunk size 1000: Tamaño del fragmento
        # Overlap 200: Solapamiento para no perder contexto entre cortes
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        
        # 3. Inicializar el modelo de Embeddings (Ollama)
        # Usamos 'nomic-embed-text' que es especialista en esto
        embedding_function = OllamaEmbeddings(
            model=settings.EMBEDDING_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        
        # 4. Guardar en ChromaDB (Base de datos vectorial local)
        # Esto crea la carpeta 'chroma_db' automáticamente si no existe
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embedding_function,
            persist_directory=settings.CHROMA_DB_DIR,
            collection_name=settings.COLLECTION_NAME
        )
        
        return {
            "status": "success", 
            "chunks_created": len(splits),
            "message": f"Documento procesado exitosamente. Se crearon {len(splits)} fragmentos."
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def clean_temp_file(path: str):
    """Elimina el archivo temporal después de procesarlo"""
    if os.path.exists(path):
        os.remove(path)