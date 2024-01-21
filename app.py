from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import fastapi as _fapi

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
async def find(imgPromptCreate: _schemas.ImageCreate = _fapi.Depends()):
    
    try:
        image = await _services.generate_image(imgPrompt=imgPromptCreate)
    except Exception as e:
        print(traceback.format_exc())
        return {"message": f"{e.args}"}

    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    return StreamingResponse(memory_stream, media_type="image/png")
