import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Stencil Pro", page_icon="🖊️")

st.title("🖊️ Stencil Pro - Tattoo")
st.write("Tire uma foto ou escolha da galeria.")

# --- BARRA LATERAL ---
st.sidebar.header("Ajustes")
nivel_detalhe = st.sidebar.slider("Nível de Limpeza (C)", 2, 10, 3)

# --- FUNÇÃO DE PROCESSAMENTO ---
def processar_stencil(image_bytes, c_value):
    # Decodifica a imagem
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Processamento
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    stencil = cv2.adaptiveThreshold(blurred, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, c_value)
    return img, stencil

# --- ESCOLHA A FONTE DA IMAGEM ---
# Adicionamos abas para ficar organizado: Câmera ou Arquivo
tab1, tab2 = st.tabs(["📷 Câmera", "📂 Galeria"])

imagem_para_processar = None

with tab1:
    camera_pic = st.camera_input("Tire uma foto do desenho")
    if camera_pic:
        imagem_para_processar = camera_pic

with tab2:
    arquivo_pic = st.file_uploader("Escolha um arquivo", type=['jpg', 'jpeg', 'png'])
    if arquivo_pic:
        imagem_para_processar = arquivo_pic

# --- SE TIVER IMAGEM, PROCESSA ---
if imagem_para_processar is not None:
    original, resultado = processar_stencil(imagem_para_processar, nivel_detalhe)
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.image(original, caption="Original", channels="BGR")
    with col2:
        st.image(resultado, caption="Stencil")
    
    # Botão de Download
    is_success, buffer = cv2.imencode(".jpg", resultado)
    io_buf = io.BytesIO(buffer)
    
    st.download_button(label="⬇️ Baixar Stencil", data=io_buf, file_name="stencil.jpg", mime="image/jpeg")
