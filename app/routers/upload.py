import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vector_db import process_and_store_pdf, clean_temp_file

router = APIRouter()

# Creamos una carpeta temporal para guardar los archivos mientras se procesan
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", summary="Subir y procesar un PDF")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint para subir un PDF.
    1. Guarda el archivo temporalmente.
    2. Lo procesa (Embedding + Vector DB).
    3. Elimina el archivo temporal.
    """
    # Validar que sea PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    # Ruta temporal del archivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # 1. Guardar archivo en disco
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Procesar con nuestra lógica de RAG
        result = process_and_store_pdf(file_path)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 3. Limpieza siempre (incluso si falla)
        clean_temp_file(file_path)