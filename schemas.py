import pydantic as _pydantic
from typing import Optional
from fastapi import UploadFile


class _QueryBase(_pydantic.BaseModel):
    encoded_base_img: UploadFile
