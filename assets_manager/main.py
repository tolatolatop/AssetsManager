#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 16:27
# @Author  : tolatolatop
# @File    : main.py
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
