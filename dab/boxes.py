# AUTOGENERATED! DO NOT EDIT! File to edit: boxes.ipynb (unless otherwise specified).

__all__ = ['dtd', 'dtd', 'vslzr', 'model_config_path', 'model_checkpoint_path', 'device', 'args', 'checkpoint', 'model',
           'get_boxes']

# Cell

import os, sys
import torch
import numpy as np

from models import build_DABDETR, build_dab_deformable_detr
from util.slconfig import SLConfig
from datasets import build_dataset
from util.visualizer import COCOVisualizer
from util import box_ops

from PIL import Image
import datasets.transforms as T
import requests, io
import requests
from .paths import *

from .segment import *
import requests
from PIL import Image
from io import BytesIO


vslzr = COCOVisualizer()

def dtd(d,device):
    return {k: v.to(device=device, non_blocking=True) if hasattr(v, 'to')
               else dtd(v,device) if hasattr(v, 'items')
               else [dtd(i,device) for i in v] if isinstance(v,list)
               else v for k, v in d.items()}
model_config_path     = "model_zoo/DAB_DETR/R50_v2/config.json" # change the path of the model config file
model_checkpoint_path = "model_zoo/DAB_DETR/R50_v2/checkpoint.pth" # change the path of the model checkpoint
# See our Model Zoo section in README.md for more details about our pretrained models.

device='cpu'
args = SLConfig.fromfile(model_config_path)
model, criterion, postprocessors = build_dab_deformable_detr(args)
checkpoint = torch.load(model_checkpoint_path, map_location=device)
model.load_state_dict(checkpoint['model'])
model = model.to('cuda')
def dtd(d,device):
    return {k: v.to(device=device, non_blocking=True) if hasattr(v, 'to')
               else dtd(v,device) if hasattr(v, 'items')
               else [dtd(i,device) for i in v] if isinstance(v,list)
               else v for k, v in d.items()}

# Cell
def get_boxes(image,thershold=35):

    image_init = image



    # image
    # transform images
    transform = T.Compose([
        T.RandomResize([800], max_size=1333),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image, _ = transform(image_init, None)
    # predict images
    output = model(image[None].to('cuda'))
    output = dtd(output,'cpu')
    output = postprocessors['bbox'](output, torch.Tensor([[1.0, 1.0]]))[0]
    # visualize outputs

    scores = output['scores']
    labels = output['labels']
    boxes = box_ops.box_xyxy_to_cxcywh(output['boxes'])
    select_mask = scores > thershold

    # box_label = [id2name[int(item)] for item in labels[select_mask]]
    pred_dict = {
        'boxes': boxes[select_mask],
        'size': torch.Tensor([image.shape[1], image.shape[2]]),
        # 'box_label': box_label
    }
    # vslzr.visualize(image, pred_dict, savedir=None)
    W,H = image_init.size

    boxes = []

    for box in pred_dict['boxes']:
        unnormbbox = box * torch.Tensor([W, H, W, H])
        unnormbbox[:2] -= unnormbbox[2:] / 2
        [bbox_x, bbox_y, bbox_w, bbox_h] = unnormbbox.tolist()

        boxes.append((bbox_x,bbox_y,bbox_x+bbox_w,bbox_y+bbox_h))


    return boxes

    #