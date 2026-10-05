from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path

from app.ai.gemini_flash import generate_comic_story
from app.ai.image_generator import generate_image

router = APIRouter()


class ComicRequest(BaseModel):
    prompt: str


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("templates/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/generate-comic/json")
async def generate_comic(data: ComicRequest):
    # Generate the comic story using Gemini
    result = generate_comic_story(data.prompt)

    # Stop if Gemini returns an error
    if "error" in result:
        return result

    generated_images = []

    # Create one AI image for each comic panel
    for panel in result.get("panels", []):
        panel_number = panel.get("panel", 1)
        scene = panel.get("scene", "")

        image_prompt = f"""
Create a colorful children's comic-book illustration.

Scene:
{scene}

Style:
- vibrant comic art
- expressive characters
- cinematic composition
- magical adventure atmosphere
- clean detailed illustration
- no text
- no watermark
"""

        output_path = (
            Path("generated_images")
            / f"panel_{panel_number}.png"
        )

        try:
            image_path = generate_image(
                image_prompt,
                str(output_path)
            )

            generated_images.append({
                "panel": panel_number,
                "image": f"/images/panel_{panel_number}.png"
            })

        except Exception as exc:
            generated_images.append({
                "panel": panel_number,
                "image": None,
                "error": str(exc)
            })

    # Add generated image information to the response
    result["images"] = generated_images

    return result