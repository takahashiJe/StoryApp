from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_gif
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import torch
import os
import uvicorn
import glob

app = FastAPI(root_path="/api")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Change this to specific origins in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the request model
class StoryRequest(BaseModel):
    stories: list[str]

# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float32  # Use float32 as float16 might not be supported on CPU

# Animation Diffusion Pipeline configuration
step = 8  # Number of steps for the animation diffusion
repo = "ByteDance/AnimateDiff-Lightning"
ckpt = f"animatediff_lightning_{step}step_diffusers.safetensors"
base = "emilianJR/epiCRealism"  # Base model for animation

# Load the motion adapter and pipeline
adapter = MotionAdapter().to(device, dtype)
adapter.load_state_dict(load_file(hf_hub_download(repo, ckpt), device=device))
pipe = AnimateDiffPipeline.from_pretrained(base, motion_adapter=adapter, torch_dtype=dtype).to(device)
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing", beta_schedule="linear")

@app.post("/generate-gif")
async def generate_gif(request: StoryRequest):
    """
    Generate GIFs from the provided stories.
    """
    try:
        files = glob.glob(os.path.join("static", '*'))
        for file in files:
            os.remove(file)
        gif_urls = []
        for i, story in enumerate(request.stories):
            prompt = story
            output = pipe(prompt=prompt, guidance_scale=1.0, num_inference_steps=step)
            gif_path = f"./static/animation_{i}.gif"
            export_to_gif(output.frames[0], gif_path)
            gif_urls.append(f"/static/{os.path.basename(gif_path)}")
        return {"gifUrls": gif_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/static/{gif_name}")
async def get_gif(gif_name: str):
    """
    Retrieve a generated GIF by its name.
    """
    gif_path = f"./static/{gif_name}"
    if os.path.exists(gif_path):
        return FileResponse(gif_path)
    raise HTTPException(status_code=404, detail="GIF not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
