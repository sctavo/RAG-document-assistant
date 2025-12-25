from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from app.core.config import settings

# 1. Configurar el LLM
llm = ChatOllama(
    model=settings.OLLAMA_MODEL, 
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0.1 # Muy baja temperatura para que sea robotico y preciso
)

# 2. Configurar Embeddings
embedding_function = OllamaEmbeddings(
    model=settings.EMBEDDING_MODEL,
    base_url=settings.OLLAMA_BASE_URL
)

# 3. Prompt Template (Instrucciones a prueba de tontos)
# Usamos un prompt más directo para evitar que se confunda.
template = """
Instrucción: Eres un asistente técnico. Responde la pregunta basándote SOLAMENTE en el siguiente contexto.
Si la respuesta no está en el contexto, di "No lo sé".

Contexto:
{context}

Pregunta: 
{question}

Respuesta útil:
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    """
    Función de Limpieza:
    Toma los documentos recuperados (que vienen llenos de metadatos basura)
    y extrae SOLO el texto del contenido (page_content).
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_answer(question: str):
    
    # Conectar a la BD
    vectorstore = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embedding_function,
        collection_name=settings.COLLECTION_NAME
    )
    
    # Retriever: k=3 para tener suficiente contexto pero no saturar
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Cadena de procesamiento (Chain)
    rag_chain = (
        # Aquí aplicamos la limpieza 'format_docs' antes de pasar el texto al prompt
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain.invoke(question)