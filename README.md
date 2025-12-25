# 🧠 NeuralDoc: Local RAG System

> **Asistente inteligente de documentación técnica que respeta tu privacidad.**
> *Ejecutado 100% localmente con LLMs Open Source (TinyLlama/Phi-3).*

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C?logo=langchain)
![Ollama](https://img.shields.io/badge/AI-Ollama-000000?logo=ollama)

## 📖 Descripción

**NeuralDoc** es un sistema de **Retrieval-Augmented Generation (RAG)** diseñado para ingenieros, estudiantes y profesionales que necesitan consultar manuales técnicos, papers de investigación o documentación legal extensa sin depender de la nube.

A diferencia de soluciones comerciales como GPT-4, NeuralDoc corre **on-premise** (en tu propia máquina), garantizando que tus datos privados nunca salgan de tu ordenador y sin costes por token.

Características de Ingeniería
Ingeniería de Prompts (Zero-shot): Optimización de instrucciones específicas para "Small Language Models" (SLMs) para reducir alucinaciones y mejorar la precisión sin necesitar modelos pesados.

Búsqueda Vectorial Eficiente: Implementación de ChromaDB persistente con particionamiento de textos (Chunking) optimizado para documentos técnicos.

Optimización de Recursos (CPU-First): Diseñado para correr en laptops estándar. Tiempo de respuesta optimizado (<20s) utilizando modelos cuantizados (TinyLlama/Phi-3).

Clean Architecture: Separación modular de responsabilidades:

routers/: Endpoints de la API.

services/: Lógica de negocio (RAG, ETL).

core/: Configuraciones y variables de entorno.

🚀 Instalación y Despliegue
Prerrequisitos
Python 3.10+ instalado.

Ollama instalado y corriendo en segundo plano.

1. Clonar el repositorio
Bash
git clone [https://github.com/tu-usuario/neural-doc.git](https://github.com/tu-usuario/neural-doc.git)
cd neural-doc

2. Configurar el entorno virtual
Es recomendable usar un entorno aislado para las dependencias.

Bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
Bash
pip install -r requirements.txt

4. Configurar Modelos de IA (Ollama)
Descarga los modelos optimizados para ejecución local:
Bash
# Modelo de lenguaje (Cerebro) - Opción rápida
ollama pull tinyllama
# Modelo de Embeddings (Motor de búsqueda vectorial)
ollama pull nomic-embed-text


5. Variables de Entorno
Crea un archivo .env en la raíz del proyecto (basado en el ejemplo):

Ini, TOML

PROJECT_NAME="Neural Doc Search"
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="tinyllama"
CHROMA_DB_DIR="chroma_db"
🛠️ Ejecución
El sistema requiere dos terminales ejecutándose simultáneamente:



Terminal 1: Backend (API)
Bash
uvicorn app.main:app --reload
# La API estará disponible en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


Terminal 2: Frontend (UI)
Bash
streamlit run frontend.py
# La interfaz web se abrirá automáticamente en http://localhost:8501


📂 Estructura del Proyecto

📦 NeuralDoc
 ┣ 📂 app
 ┃ ┣ 📂 core         # Configuración (Settings, .env)
 ┃ ┣ 📂 routers      # Endpoints (Chat, Upload)
 ┃ ┣ 📂 services     # Lógica RAG y Vector DB
 ┃ ┗ 📜 main.py      # Entry point FastAPI
 ┣ 📜 frontend.py    # Interfaz de usuario (Streamlit)
 ┣ 📜 requirements.txt
 ┣ 📜 docker-compose.yml
 ┗ 📜 README.md


🤝 Contribuciones
Este proyecto fue desarrollado como parte de un portafolio de Ingeniería Civil en Computación. Las sugerencias y Pull Requests son bienvenidos.

Hecho con 🐍 y ☕ por Gustavo Sanchez