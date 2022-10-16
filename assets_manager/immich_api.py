#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 17:16
# @Author  : tolatolatop
# @File    : immich_api.py
import os
import urllib.parse

import requests
import requests as rq
from fastapi import HTTPException

immich_host = os.environ["IMMICH_HOST"]
agent_email = os.environ["AGENT_EMAIL"]
agent_password = os.environ["AGENT_PASSWORD"]


def get_session_of_immich():
    session = rq.Session()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*"
    }
    session.headers = headers

    return session


def login(session, email, password):
    api_path = urllib.parse.urljoin(immich_host, "api/auth/login")
    body = {
        "email": email,
        "password": password
    }

    res = session.post(api_path, json=body)
    return res.json()


def get_all_albums(session):
    api_path = urllib.parse.urljoin(immich_host, "api/album")
    res: requests.Response = session.get(api_path)
    return res.json()


def get_album_info(session, album_name):
    api_path = urllib.parse.urljoin(immich_host, "api/album")

    res: requests.Response = session.get(api_path)
    if res.status_code == 200:
        data = res.json()
        for d in data:
            if d["albumName"] == album_name:
                return d
        raise HTTPException(status_code=404, detail="Item not found")
    return res.json()


def get_all_album_assets(session, album_id):
    api_path = urllib.parse.urljoin(immich_host, f"api/album/{album_id}")

    res: requests.Response = session.get(api_path)
    if res.status_code == 200:
        data = res.json()
        return data["assets"]
    return res.json()


def download_file_to_disk(session, asset_id, dir_path):
    api_path = urllib.parse.urljoin(immich_host, f"api/asset/download")
    params = {
        "aid": asset_id,
        "did": "WEB",
        "isThumb": False,
        "isWeb": False
    }

    res: requests.Response = session.get(api_path, params=params)
    if res.status_code == 200:
        data = res.content
        return data
    raise HTTPException(status_code=404, detail="Item not found")
