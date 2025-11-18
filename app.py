import streamlit as st
import os
from PIL import Image
from tryon import run_tryon

st.set_page_config(page_title="Virtual TryOn", layout="wide")

INPUT_DIR = "input"
CLOTH_DIR = "clothes"
HISTORY_DIR = "history"

os.makedirs(HISTORY_DIR, exist_ok=True)

st.title("🧪 Essayage Virtuel - Interface Avancée")

# ---- COLONNES ----
col_user, col_cloth, col_preview = st.columns([1,1,2])

# ---- Upload utilisateur ----
with col_user:
    st.subheader("📸 Photo utilisateur")
    user_file = st.file_uploader("Choisis une photo", type=["png","jpg","jpeg"])
    if user_file:
        user_img = Image.open(user_file).convert("RGB")
        st.image(user_img, caption="Photo utilisateur", use_container_width=True)
        user_path = os.path.join(INPUT_DIR, "user.png")
        user_img.save(user_path)

# ---- Catalogue vêtements ----
with col_cloth:
    st.subheader("👕 Catalogue de vêtements")

    clothes = [f for f in os.listdir(CLOTH_DIR) if f.lower().endswith(("png","jpg","jpeg"))]

    if not clothes:
        st.warning("Ajoute des vêtements dans le dossier clothes/")
    else:
        cloth_choice = st.selectbox("Choisis un vêtement", clothes)
        cloth_path = os.path.join(CLOTH_DIR, cloth_choice)
        st.image(cloth_path, caption="Vêtement choisi", use_container_width=True)

# ---- Zone Prévisualisation / Résultat ----
with col_preview:
    st.subheader("🖼 Aperçu rendu")

    if st.button("🔮 Générer le rendu"):
        if user_file and cloth_choice:
            output_path = os.path.join(HISTORY_DIR, "result.png")
            with st.spinner("Génération en cours..."):
                result = run_tryon(user_path, cloth_path, output_path)
            st.success("Rendu généré !")
            st.image(result, caption="Résultat", use_container_width=True)
        else:
            st.error("Ajoute une photo utilisateur et choisis un vêtement")

# ---- Historique ----
st.subheader("📚 Historique")

history_files = sorted(os.listdir(HISTORY_DIR))
for h in history_files:
    st.image(os.path.join(HISTORY_DIR, h), width=150)
