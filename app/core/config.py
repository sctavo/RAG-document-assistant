import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carga explícita del archivo .env
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAG API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    
    # Configuración de Ollama (Gratis/Local)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    EMBEDDING_MODEL: str = "nomic-embed-text"  # El modelo ligero que estamos bajando
    
    # Configuración de Base de Datos Vectorial
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "chroma_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "rag_docs")

settings = Settings()