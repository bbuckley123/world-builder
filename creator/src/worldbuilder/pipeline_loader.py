from functools import lru_cache
import torch
from diffusers import StableDiffusion3Pipeline

@lru_cache(maxsize=1)
def get_stable_diffusion_pipeline() -> StableDiffusion3Pipeline:
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3-medium-diffusers",
        text_encoder_3=None,
        tokenizer_3=None,
        torch_dtype=torch.float16,
        feature_extractor=None,
        local_files_only=True
    ).to(device)

    pipe.enable_attention_slicing()
    return pipe
