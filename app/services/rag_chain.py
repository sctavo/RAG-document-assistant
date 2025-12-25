from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from app.core.config import settings

# 1. Configurar el LLM (El cerebro que habla)
llm = ChatOllama(
    model=settings.OLLAMA_MODEL, 
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0  # 0 para que sea preciso y no invente
)

# 2. Configurar los Embeddings (Para buscar en la BD)
embedding_function = OllamaEmbeddings(
    model=settings.EMBEDDING_MODEL,
    base_url=settings.OLLAMA_BASE_URL
)

# 3. Prompt Template (Las instrucciones para la IA)
# Le decimos: "Eres un asistente. Usa SOLO el contexto para responder."
template = """
Eres un asistente de IA experto en analizar documentos técnicos.
Usa los siguientes fragmentos de contexto recuperado para responder la pregunta al final.
Si no sabes la respuesta basándote en el contexto, di simplemente "No encuentro esa información en el documento".
Manten la respuesta concisa.

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""
prompt = ChatPromptTemplate.from_template(template)

def get_answer(question: str):
    """
    Función principal del RAG:
    1. Embedde la pregunta.
    2. Busca en ChromaDB los fragmentos más parecidos.
    3. Envía todo al LLM.
    """
    
    # Conectar a la BD existente
    vectorstore = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embedding_function,
        collection_name=settings.COLLECTION_NAME
    )
    
    # Convertir la BD en un "Retriever" (Buscador)
    # k=2 significa "traeme los 2 fragmentos más relevantes"
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # Definir la cadena (Chain) de procesamiento
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Ejecutar
    return rag_chain.invoke(question)