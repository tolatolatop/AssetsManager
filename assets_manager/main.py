#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 16:27
# @Author  : tolatolatop
# @File    : main.py
from typing import Union

from fastapi import FastAPI

import immich_api
import config

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


@app.get("/immich/agent/albums")
def agent_albums():
    session = immich_api.get_session_of_immich()
    res = immich_api.login(session, immich_api.agent_email, immich_api.agent_password)
    res = immich_api.get_all_albums(session)
    return res


@app.get("/immich/agent/albums/{album_name}")
def agent_album(album_name: str):
    session = immich_api.get_session_of_immich()
    immich_api.login(session, immich_api.agent_email, immich_api.agent_password)
    res = immich_api.get_album_info(session, album_name)
    return res


@app.get("/immich/agent/albums/{album_name}/assets")
def agent_albums_assets(album_name: str):
    session = immich_api.get_session_of_immich()
    res = immich_api.login(session, immich_api.agent_email, immich_api.agent_password)
    res = immich_api.get_album_info(session, album_name)
    album_id = res["id"]
    res = immich_api.get_all_album_assets(session, album_id)
    return res
