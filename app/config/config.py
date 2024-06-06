# -*- coding:utf-8 -*-
"""
@file: config.py
@author: June
@date: 2024/3/1
@IDE: vscode
"""
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List


class Setting(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    CRAWL_URLS: List[AnyHttpUrl] = [
        "https://xdz.xa.gov.cn/xwzx/tzgg/1.html",
        "http://scjg.xa.gov.cn/xwzx/tzgg/1.html",
        "http://gxt.shaanxi.gov.cn/webfile/tzgg/",
        "https://shxca.miit.gov.cn/xwzx/tzgg/"
    ]

    PROJECT_NAME: str = "CrawlData"
    DESCRIPTION: str = "crawl data with spider"

    # api
    API_V1_STR: str = "/api"
    IS_DEV: bool

    # log
    LOG_DIR: str = "logs/crawl_data{time}.log"
    LOG_LEVEL: str

    # HEADERS
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # gradio
    CUSTOM_PATH: str

    # LLM
    LLM_HOST: str
    LLM_PORT: int

    # EMBEDDING
    # EMBEDDING_HOST: str
    # EMBEDDING_PORT: int

    # File Path
    FILE_PATH: str = "app/static/docs"


settings = Setting()
