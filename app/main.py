from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Iniciar la aplicación con metadatos
# Estos datos aparecerán en la documentación automática (/docs)
app = FastAPI(
    title="Neural Doc Search API",
    description="Backend para sistema RAG (Retrieval-Augmented Generation) con LangChain y ChromaDB",
    version="0.1.0",
)

# 2. Configuración de CORS (Cross-Origin Resource Sharing)
# permite que el frontend (Streamlit/React) que corre en un puerto
# pueda comunicarse con este backend que corre en otro.
# En producción, 'allow_origins' debería ser la URL específica de frontend, no "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ok para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],
)

# 3. Health Check (Endpoint Raíz)
# Un endpoint simple para verificar que el servidor está vivo.
@app.get("/", tags=["General"])
async def root():
    return {
        "status": "ok",
        "message": "El sistema RAG está activo y listo para recibir peticiones.",
        "documentation": "/docs"
    }

# 4. Futura Integración de Routers
# Aquí se conecta la lógica de chat y upload cuando se escriba.
# De momento queda comentado para que no de error.
# from app.routers import chat, upload
# app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
# app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])