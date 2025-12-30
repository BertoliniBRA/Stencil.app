import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Stencil Pro", page_icon="🖊️", layout="wide")

st.title("🖊️ Stencil Pro - Tattoo Converter")
st.markdown("Converta fotos em decalque pronto para impressão térmica.")

# Upload
uploaded_file = st.file_uploader("Carregue a imagem (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Ler imagem
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Processamento Base
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Criar as 3 versões automaticamente
    # 1. Grosso (Original)
    stencil_1 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 2. Padrão (Ouro)
    stencil_2 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
    # 3. Fino (Limpo)
    stencil_3 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)

    # Mostrar na tela
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(stencil_1, caption="Opção 1: Traço Forte", use_column_width=True)
        is_success, buffer1 = cv2.imencode(".jpg", stencil_1)
        st.download_button(label="⬇️ Baixar Opção 1", data=io.BytesIO(buffer1), file_name="stencil_forte.jpg", mime="image/jpeg")

    with col2:
        st.image(stencil_2, caption="Opção 2: Padrão Ouro", use_column_width=True)
        is_success, buffer2 = cv2.imencode(".jpg", stencil_2)
        st.download_button(label="⬇️ Baixar Opção 2", data=io.BytesIO(buffer2), file_name="stencil_padrao.jpg", mime="image/jpeg")

    with col3:
        st.image(stencil_3, caption="Opção 3: Traço Fino", use_column_width=True)
        is_success, buffer3 = cv2.imencode(".jpg", stencil_3)
        st.download_button(label="⬇️ Baixar Opção 3", data=io.BytesIO(buffer3), file_name="stencil_fino.jpg", mime="image/jpeg")

else:
    st.info("👆 Faça o upload para gerar as opções.")
