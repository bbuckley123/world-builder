#!/usr/bin/env python3
import argparse
import torch
from PIL import Image
from diffusers import StableDiffusionInpaintPipeline

def main():
    # 1) Parse CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", "-i", required=True,
                        help="Path to your input image (e.g. your photo)")
    parser.add_argument("--prompt", "-p", required=True,
                        help="Text to guide the new haircut")
    parser.add_argument("--output", "-o", default="out.png",
                        help="Where to save the result")
    args = parser.parse_args()

    # 2) Device & pipeline
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-inpainting",
        torch_dtype=torch.float32,
        safety_checker=None,
        requires_safety_checker=False
    ).to(device)
    pipe.enable_attention_slicing()

    # 3) Load & preprocess your photo
    init_image = Image.open(args.init).convert("RGB")
    mask_image = Image.new("L", init_image.size, 255)  # mode "L" = 8-bit grayscale; 255=white

    # 4) Run img2img
    # strength=0.7 means “70% new content, 30% original preserved”
    result = pipe(
        prompt=args.prompt,
        image=init_image,
        mask_image=mask_image,
        strength=0.7,
        guidance_scale=7.5,
        num_inference_steps=50
    )
    result.images[0].save(args.output)
    print(f"✅ Saved to {args.output}")

if __name__ == "__main__":
    main()
