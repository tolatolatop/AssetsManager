#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 17:16
# @Author  : tolatolatop
# @File    : immich_api.py
import os
import pathlib
import urllib.parse

import requests
import requests as rq
from fastapi import HTTPException

immich_host = os.environ["IMMICH_HOST"]
agent_email = os.environ["AGENT_EMAIL"]
agent_password = os.environ["AGENT_PASSWORD"]
agent_root_path = "/root/assets"


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


def get_assert_data(session, asset_id):
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


def get_album_id(session, album_name):
    res = get_album_info(session, album_name)
    album_id = res["id"]
    return album_id


def download_assets_in_album(session, album_name):
    album_id = get_album_id(session, album_name)
    assets = get_all_album_assets(session, album_id)

    album_path = pathlib.Path(agent_root_path) / album_name

    if not album_path.exists():
        album_path.mkdir(exist_ok=True, parents=True)

    for asset in assets:
        asset_id = asset["deviceAssetId"]
        remote_path = asset["originalPath"]
        file_name = os.path.basename(remote_path)
        asset_path = album_path / file_name
        if not asset_path.exists():
            data = get_assert_data(session, asset_id)
            with asset_path.open("wb") as f:
                f.write(data)
    return {"status": "ok", "album_path": str(album_path.absolute())}
