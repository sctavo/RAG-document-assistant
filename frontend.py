import streamlit as st
import requests

# --- Configuración Inicial ---
st.set_page_config(
    page_title="NeuralDoc | RAG System",
    page_icon="⚡",
    layout="wide"
)

# --- INYECCIÓN CSS (ESTILO PROFESIONAL) ---
# Esto oculta los bordes feos y da un look "Dark Mode SaaS"
st.markdown("""
<style>
    /* Fondo principal y colores de texto */
    .stApp {
        background-color: #0e1117;
        color: #FAFAFA;
    }
    
    /* Input de Chat Estilizado */
    .stChatInputContainer textarea {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #4B4B4B;
    }
    
    /* Mensajes del Chat */
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #363636;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161a24;
        border-right: 1px solid #363636;
    }
    
    /* Botones */
    .stButton button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #FF2B2B;
        border-color: #FF2B2B;
    }
    
    /* Títulos */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# URL del Backend
API_URL = "http://127.0.0.1:8000/api"

# --- SIDEBAR (PANEL DE CONTROL) ---
with st.sidebar:
    st.title("⚡ NeuralDoc")
    st.markdown("---")
    
    st.subheader("📂 Base de Conocimiento")
    uploaded_file = st.file_uploader("Arrastra tu PDF aquí", type="pdf")
    
    if uploaded_file:
        col1, col2 = st.columns([1,1])
        with col1:
            process_btn = st.button("Procesar", use_container_width=True)
        
        if process_btn:
            with st.status("Ingestando datos...", expanded=True) as status:
                try:
                    st.write("📤 Subiendo archivo...")
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post(f"{API_URL}/upload/", files=files)
                    
                    if response.status_code == 200:
                        st.write("🧩 Generando vectores (Embeddings)...")
                        st.write("💾 Guardando en ChromaDB...")
                        status.update(label="¡Listo! Documento aprendido.", state="complete", expanded=False)
                        st.toast("Documento indexado con éxito", icon="✅")
                    else:
                        status.update(label="Error en el proceso", state="error")
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

    st.markdown("---")
    st.caption("Backend: FastAPI + LangChain")
    st.caption("Model: TinyLlama / Ollama")
    
    if st.button("Limpiar Conversación", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# --- ÁREA PRINCIPAL ---
st.title("Asistente Técnico")
st.markdown("Haz preguntas sobre tus documentos PDF cargados. El sistema buscará referencias exactas.")

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderizar chat anterior
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu pregunta técnica..."):
    # Guardar y mostrar user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Respuesta del bot
    with st.chat_message("assistant", avatar="⚡"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analizando documentos...")
        
        try:
            # Petición al API
            response = requests.post(f"{API_URL}/chat/", json={"question": prompt})
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                message_placeholder.error("Error en el servidor Neural.")
        except Exception as e:
            message_placeholder.error(f"No se pudo conectar con el API. ¿Está corriendo uvicorn? Error: {e}")