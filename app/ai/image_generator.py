import os
from pathlib import Path

import torch
from diffusers import DiffusionPipeline
from dotenv import load_dotenv

load_dotenv()


MODEL_ID = "segmind/tiny-sd"

# Load the model only once
_pipeline = None


def get_pipeline():
    global _pipeline

    if _pipeline is None:
        print("Loading Tiny-SD model for CPU...")

        _pipeline = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float32
        )

        _pipeline = _pipeline.to("cpu")

        # Reduce memory usage on CPU
        try:
            _pipeline.enable_attention_slicing()
        except Exception:
            pass

        print("Tiny-SD model loaded.")

    return _pipeline


def generate_image(
    prompt: str,
    output_path: str = "generated_images/panel.png"
) -> str:

    pipe = get_pipeline()

    comic_prompt = f"""
A colorful children's comic-book illustration.

Scene:
{prompt}

Style:
clean comic art, colorful, fantasy adventure,
expressive characters, magical forest,
friendly character design, detailed background,
storybook illustration, polished artwork
"""

    print("Generating AI image...")

    result = pipe(
        prompt=comic_prompt,
        height=384,
        width=384,
        num_inference_steps=10,
        guidance_scale=7.5
    )

    image = result.images[0]

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    image.save(output_file)

    print(f"Image saved to: {output_file}")

    return str(output_file)