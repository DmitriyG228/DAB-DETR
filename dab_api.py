#cd; conda activate dab; cd DAB-DETR; uvicorn dab_api:app --port 8184 & disown
#cd; conda activate clipapi; cd clipapi; uvicorn model_api:app --port 8182 &>>$HOME/output/api.log

# from clip.tools import get_logger



try:
    logger = get_logger('model_api')
    logger.debug('loading')
except:
    logger = None


import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

from fastapi import BackgroundTasks, FastAPI
from starlette.middleware.cors import CORSMiddleware

from dab.boxes import get_boxes


from PIL import Image
import requests

app = FastAPI(title="get_boxes", version="0.2",)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



@app.post("/get_boxes/")
async def boxes(url: str):
    if logger:logger.debug(f'get_boxes {url}')
    response = requests.get(url, stream=True)
    image = Image.open(response.raw)
    return  get_boxes(image)

if logger: logger.debug('up')

    


