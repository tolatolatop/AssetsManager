#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/16 17:16
# @Author  : tolatolatop
# @File    : immich_api.py
import os
import urllib.parse

import requests as rq

immich_host = os.environ["IMMICH_HOST"]


def get_session_of_immich():
    session = rq.Session()
    headers = {
        "contentTypes": "application/json"
    }
    session.headers = headers

    return session


def login(session, email, password):
    api_path = urllib.parse.urljoin(immich_host, "api/auth/login")
    body = {
        "email": email,
        "password": password
    }

    res = session.post(api_path, body=body)
    return res.json()
