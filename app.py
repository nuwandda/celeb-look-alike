from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.responses import Response
import fastapi as _fapi
import base64

import schemas as _schemas
import services as _services
import io
import traceback


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Celeb Look-alike API"}

# Endpoint to test the backend
@app.get("/api")
async def root():
    return {"message": "Welcome to the Look-alike with FastAPI"}

@app.post("/api/find/")
async def find(query: _schemas._QueryBase = _fapi.Depends()):
    
    try:
        image, name = await _services.find_look_alike(query=query)
    except Exception as e:
        print(traceback.format_exc())
        return {"message": f"{e.args}"}

    # memory_stream = io.BytesIO()
    # image.save(memory_stream, format="PNG")
    # memory_stream.seek(0)
    encoded_img = base64.b64encode(image)
    payload = {
       "mime" : "image/jpg",
       "image": encoded_img,
       "name": name
   }
    # return StreamingResponse(memory_stream, media_type="image/png")
    return payload
