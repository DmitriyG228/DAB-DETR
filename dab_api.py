#cd; conda activate dab; cd DAB-DETR; uvicorn dab_api:app --port 8185 & disown
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

from dab.box_segment import *

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
async def boxes(url: str,thershold: float = 0.35):
    return  save_segmented_boxes(url,thershold)

if logger: logger.debug('up')

    


