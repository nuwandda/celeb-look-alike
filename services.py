import schemas as _schemas
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import numpy as np
from pkg_resources import parse_version
import utils
import uuid
import cv2
import wikipedia_downloader


load_dotenv()
 
"""
Note: make sure .env exist and contains your token
"""
df = utils.load_metadata('/home/tinbicen/Downloads/wiki/wiki.mat')


async def find_look_alike(query: _schemas._QueryBase) -> Image:
    temp_id = str(uuid.uuid4())
    utils.create_temp()
    
    request_object_content = await query.encoded_base_img.read()
    init_image = Image.open(BytesIO(request_object_content))
    init_image = init_image.save(utils.TEMP_PATH + '/' + temp_id + '.jpg')
    
    result = utils.find_similar_face(utils.TEMP_PATH + '/' + temp_id + '.jpg', df, query.gender)
    upscaled_image = wikipedia_downloader.get_image(result['name'], temp_id)
    upscaled_image = utils.crop_face(upscaled_image)
    utils.remove_temp_image(temp_id)
    _, im_png = cv2.imencode(".jpg", upscaled_image)
    
    return im_png, result['name']
    
        