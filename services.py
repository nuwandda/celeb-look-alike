import schemas as _schemas

import torch 
from diffusers import StableDiffusionImg2ImgPipeline
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from utils import set_seed, eye_color_new, gender
import numpy as np
from pkg_resources import parse_version
import chromadb
import face_recognition


load_dotenv()

# Get the token from HuggingFace 
"""
Note: make sure .env exist and contains your token
"""
MODEL_PATH = os.getenv('MODEL_PATH')
if MODEL_PATH is None:
    MODEL_PATH = 'weights/rcnzCartoon3d_v20.safetensors'


async def find_look_alike(imgPrompt: _schemas.ImageCreate) -> Image:
    pass
        