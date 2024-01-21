import pydantic as _pydantic
from typing import Optional
from fastapi import UploadFile


class _PromptBase(_pydantic.BaseModel):
    seed: Optional[int] = 42
    num_inference_steps: int = 50
    guidance_scale: float = 7.5
    strength: float = 0.4


class ImageCreate(_PromptBase):
    prompt: str
    negative_prompt: str
    encoded_base_img: UploadFile
    img_width: int = 512
    
    
class WeightsCreate(_pydantic.BaseModel):
    model_number: int