#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 16:27
# @Author  : tolatolatop
# @File    : main.py
from typing import Union

from fastapi import FastAPI

from assets_manager import immich_api

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/immich/user")
def immich_user(email: str, password: str):
    session = immich_api.get_session_of_immich()
    res = immich_api.login(session, email, password)
    return res
