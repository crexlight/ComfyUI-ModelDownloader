import os
import requests
from urllib.parse import urlparse

class ModelDownloader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": ""}),
                "model_type": ([
                    "checkpoints",
                    "vae",
                    "loras",
                    "controlnet",
                    "upscale_models"
                ],),
                "filename": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "download"
    OUTPUT_NODE = True
    CATEGORY = "utils"

    def download(self, url, model_type, filename):
        comfy_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        models_dir = os.path.join(comfy_root, "models", model_type)
        os.makedirs(models_dir, exist_ok=True)

        if not filename:
            filename = os.path.basename(urlparse(url).path)

        save_path = os.path.join(models_dir, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"[ModelDownloader] Downloaded → {save_path}")
        return ()
