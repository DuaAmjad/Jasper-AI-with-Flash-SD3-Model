# -*- coding: utf-8 -*-
"""Jasper AI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BQkw2uNe6StsATROrPROiGxhmE7A0j0n
"""

#JASPER AI
#INTEGRATION
#BY DUA AMJAD SIPRA

pip install git+https://github.com/initml/diffusers.git@clement/feature/flash_sd3

pip install peft

from huggingface_hub import login
import torch
from diffusers import StableDiffusion3Pipeline, SD3Transformer2DModel, FlashFlowMatchEulerDiscreteScheduler
from peft import PeftModel

# Authenticate
login(token='Insert your token here')

# Load LoRA
transformer = SD3Transformer2DModel.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    subfolder="transformer",
    torch_dtype=torch.float16,
)
transformer = PeftModel.from_pretrained(transformer, "jasperai/flash-sd3")

# Pipeline
pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    transformer=transformer,
    torch_dtype=torch.float16,
    text_encoder_3=None,
    tokenizer_3=None
)

# Scheduler
pipe.scheduler = FlashFlowMatchEulerDiscreteScheduler.from_pretrained(
    "stabilityai/stable-diffusion-3-medium-diffusers",
    subfolder="scheduler",
)

pipe.to("cuda")

prompt = "A raccoon trapped inside a glass jar full of colorful candies, the background is steamy with vivid colors."
try:
    image = pipe(prompt, num_inference_steps=4, guidance_scale=0).images[0]
    image.show()
except Exception as e:
    print(f"An error occurred: {e}")

import matplotlib.pyplot as plt
import numpy as np

image_np = np.array(image)

plt.imshow(image_np)
plt.axis('off')  # Hide axes
plt.show()

