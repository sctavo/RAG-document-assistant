# 🧠 (RAG System)

Sistema de **Retrieval-Augmented Generation (RAG)** diseñado para consultas inteligentes sobre documentación técnica, leyes y manuales. Construido con una arquitectura de microservicios.

## 🚀 Tecnologías Clave
* **Backend:** Python 3.11, FastAPI (Async).
* **AI Orchestration:** LangChain.
* **Vector Database:** ChromaDB (Persistente).
* **Caching:** Redis (Para optimización de costos y latencia).
* **Containerization:** Docker & Docker Compose.

## 🏗️ Arquitectura (High Level)
[espero hacer el diagrama más adelante]

El flujo de datos sigue el patrón estándar de RAG:
1.  **Ingestion:** Parsing de PDFs -> Chunking -> Embedding (OpenAI/HuggingFace).
2.  **Storage:** Vectores almacenados en ChromaDB.
3.  **Retrieval:** Búsqueda por similitud semántica (Cosine Similarity).
4.  **Generation:** Contexto inyectado en LLM para respuesta final.
