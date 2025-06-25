#!/usr/bin/env python3
import argparse
import os
import torch
from diffusers import StableDiffusion3Pipeline

def main():
    # Parse command-line prompt
    parser = argparse.ArgumentParser(
        description="Generate an image with Hugging Face Diffusers on MPS/CPU"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        required=True,
        help="Text prompt to generate the image"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output.png",
        help="Where to save the generated image"
    )
    args = parser.parse_args()

    device = "mps" if torch.backends.mps.is_available() else "cpu"

    # Drop the T5 Text Encoder during Inference
    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3-medium-diffusers",
        text_encoder_3=None,
        tokenizer_3=None,
        torch_dtype=torch.float16,
        feature_extractor=None
    )
    pipe = pipe.to(device)

    pipe.enable_attention_slicing()

    # Warm-up pass to avoid first-pass inconsistencies on MPS
    if device == "mps":
        _ = pipe(args.prompt, num_inference_steps=1)

    result = pipe(
        prompt=args.prompt,
        negative_prompt="",
        num_inference_steps=28,
        guidance_scale=8.5,
        height=512,
        width=512
    )

    base_image = result.images[0]
    base_output = args.output
    base_image.save(base_output)
    print(f"✅ Saved base image to {base_output}")


if __name__ == "__main__":
    main()
