from diffusers import StableDiffusion3Pipeline
import torch

def generate_image(prompt: str, output_path: str = "output.png") -> str:
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3-medium-diffusers",
        text_encoder_3=None,
        tokenizer_3=None,
        torch_dtype=torch.float16,
        feature_extractor=None,
    ).to(device)

    pipe.enable_attention_slicing()

    if device == "mps":
        _ = pipe(prompt, num_inference_steps=1)

    result = pipe(
        prompt=prompt,
        negative_prompt="",
        num_inference_steps=40,
        guidance_scale=8.5,
        height=512,
        width=512
    )

    result.images[0].save(output_path)
    return output_path
