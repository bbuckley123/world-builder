from worldbuilder.pipeline_loader import get_stable_diffusion_pipeline

def generate_image(prompt: str, output_path: str = "output.png") -> str:
    pipe = get_stable_diffusion_pipeline()

    result = pipe(
        prompt=prompt,
        negative_prompt="",
        num_inference_steps=40,
        guidance_scale=8.5,
        height=512,
        width=1024
    )

    result.images[0].save(output_path)
    return output_path
