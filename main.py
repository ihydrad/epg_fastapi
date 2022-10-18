import re

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Union

app = FastAPI()
err_msg = "Not valid input data"

def prep_str(phrase: str):
    str_data = phrase.replace(" ", "+").replace("'", "").replace('"', "")
    pattern = r"((\d+\s*[-+*/]?\s*\d+)+([-+*/]?\s*\d+)*)+"
    try:
        out = re.match(pattern, str_data).group(0)
    except:
        return None    
    return out

class Item(BaseModel):
    exp: str
    res: Union[int, None] = None

@app.get("/")
async def root():
    return "Hello world"

@app.get("/eval")
async def calc(phrase: str):
    req_data = prep_str(phrase)
    if req_data:
        return f"{req_data}={eval(req_data)}"
    else:
        return PlainTextResponse(err_msg, status_code=400)
    

@app.post("/eval", status_code=201)
async def calc(item: Item):
    req_data = prep_str(item.exp)
    if req_data:
        item.res = eval(req_data)
        return item
    else:
        raise HTTPException(status_code=400, detail=err_msg)
