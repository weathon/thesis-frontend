from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import torch, torchvision
from model import * 

import deepsmiles 
from PIL import Image
import json

device = "cpu"

converter = deepsmiles.Converter(rings=True, branches=True)
def triangle_mask(size):
    mask = 1- np.triu(np.ones((1, size, size)),k=1).astype('uint8')
    mask = torch.autograd.Variable(torch.from_numpy(mask))
    return mask

def top_k_2d(m, k):
  values, indices = torch.topk(m.flatten(), k)
  return indices//m.shape[1], indices%m.shape[1]

def pad_pack(sequences):
    maxlen = max(map(len, sequences))
    batch = torch.LongTensor(len(sequences),maxlen).fill_(0)
    for i,x in enumerate(sequences):
        batch[i,:len(x)] = torch.LongTensor(x)
    return batch, maxlen

reversed_word_map = {}

with open("reverse.map","r") as f:
  reversed_word_map = json.loads(f.read())
reversed_word_map_={}

for i in reversed_word_map.keys():
  reversed_word_map_[int(i)] = reversed_word_map[i]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import os
from PIL import Image
import tempfile
import base64

def generate(img):
  global mod
  print(img.shape)
  mod = mod.train(False)
  with torch.no_grad():
    mem = mod.decoder.encoder(mod.decoder.encoder_dim(mod.encoder(img)))
    seq = torch.tensor([[77]]).to(device)
    for i in range(100):
      out = mod.decoder.decoder(seq, mem, x_mask=triangle_mask(len(seq)).to(device))[:,-1,:].squeeze(dim=1)
      id = torch.argmax(out, dim=-1)
      if id.item()==78:
        return seq
      seq = torch.concat((seq, id.unsqueeze(0)),dim=-1)
  return seq 

import numpy as np
from pydantic import BaseModel
class Code(BaseModel):
  code:str 

@app.post("/")
def submit(code: Code):
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, "wb") as f:
      f.write(base64.decodebytes(bytes(code.code.encode())))
    image = Image.open(tmp.name)
    res = generate(torch.tensor(np.array(image.convert("RGB").resize((400,400)))).unsqueeze(0).permute(0,3,1,2).to(device).to(torch.float32))
    print(res.detach().numpy())
    return converter.decode("".join([reversed_word_map_[i] for i in res[0].numpy()])).replace("<start>","")