import time
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
import os



fastpic = True
try:
    model_name = open("./Model/Model_Path.txt", "r").readlines()[1][19:]
except IndexError as e:
    raise ValueError("Model Path not Specified")
path = f"C:/sdwebui/Stable2/stable-diffusion-webui/models/Stable-diffusion/epicrealism_pureEvolutionV3.safetensors"
if not os.path.exists(path):
    raise ValueError(f"Model does not exist check if the name is right")

torch_type = torch.float16

if fastpic:
    global pipe
    pipe = StableDiffusionPipeline.from_single_file(
            path,
            torch_dtype=torch_type,
        ).to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    pipe.safety_checker = None
def generate_image(prompt):
    print(prompt)
    if fastpic == False:
        global pipe
        pipe = StableDiffusionPipeline.from_single_file(
            path,
            torch_dtype=torch_type,
        ).to("cuda")
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
        pipe.safety_checker = None


    with autocast("cuda"):
        image = pipe(prompt, num_inference_steps=25, guidance_scale=3.5, negative_prompt="lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature, deformed face, unrealistic face, distorted face")["images"]
        image = image[0]
    file_name: str = prompt.replace(" ", "_")[:40]
    print(file_name)
    image.save("images/" + file_name + ".png")
    return "./images/" + file_name + ".png"




