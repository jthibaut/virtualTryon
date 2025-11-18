import torch
from huggingface_hub import snapshot_download
from PIL import Image
import numpy as np
import cv2
import os

MODEL_DIR = "models/tryon_full"

def download_model():
    if not os.path.exists(MODEL_DIR):
        print("📥 Téléchargement du modèle TryOnDiffusion...")
        snapshot_download(
            repo_id="diffusers/tryondiffusion",
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False
        )
        print("✔ Modèle téléchargé.")

def load_image(path):
    return Image.open(path).convert("RGB")

def run_tryon(user_img_path, cloth_img_path, output_path="output.png"):
    """
    Version simplifiée du pipeline TryOnDiffusion standard.
    """
    from diffusers import StableDiffusionInpaintPipeline

    download_model()

    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        MODEL_DIR,
        torch_dtype=torch.float16
    ).to("cuda")

    user_img = load_image(user_img_path)
    cloth_img = load_image(cloth_img_path)

    # Création d'une simple segmentation approximative
    cloth_resized = cloth_img.resize((256, 256))
    mask = cloth_resized.convert("L")

    result = pipe(
        prompt="person wearing this piece of clothing realistically, high quality, sharp, natural",
        image=user_img,
        mask_image=mask
    ).images[0]

    result.save(output_path)
    return output_path