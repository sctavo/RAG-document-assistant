import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Neural Doc Search", page_icon="🧠")
st.title("🧠 Neural Doc Search")
st.markdown("Suba un manual o documento técnico y haga preguntas sobre él.")

# URLs de nuestro Backend (FastAPI)
API_URL = "http://127.0.0.1:8000/api"

# 1. Sección de Subida de Archivos (Sidebar)
with st.sidebar:
    st.header("1. Cargar Documento")
    uploaded_file = st.file_uploader("Sube tu PDF aquí", type="pdf")
    
    if st.button("Procesar PDF") and uploaded_file is not None:
        with st.spinner("Procesando e indexando documento..."):
            # Enviar archivo al backend
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_URL}/upload/", files=files)
            
            if response.status_code == 200:
                st.success("✅ Documento indexado exitosamente!")
            else:
                st.error(f"Error: {response.text}")

# 2. Sección de Chat
st.header("2. Chat con el Documento")

# Inicializar historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu pregunta sobre el documento..."):
    # Guardar y mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar al Backend para obtener respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat/", 
                    json={"question": prompt}
                )
                
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    # Guardar respuesta en historial
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Error al conectar con el cerebro de la IA.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")