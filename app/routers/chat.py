from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import get_answer

router = APIRouter()

# Definimos el modelo de datos que esperamos recibir (JSON)
class ChatRequest(BaseModel):
    question: str

@router.post("/", summary="Hacer una pregunta a los documentos")
async def chat_endpoint(request: ChatRequest):
    """
    Recibe una pregunta, busca en la base de datos vectorial
    y genera una respuesta usando el LLM local.
    """
    try:
        if not request.question:
            raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
            
        # Llamamos a nuestra lógica de RAG
        response = get_answer(request.question)
        
        return {
            "question": request.question,
            "answer": response
        }
        
    except Exception as e:
        # En producción, loguear el error real internamente
        print(f"Error en chat: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la respuesta del LLM")