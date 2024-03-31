from .subtitle import subfetch
VERSION = '3.0.0'
from .vidsrcme import get as vidsrcmeget
from .vidsrcto import get as vidsrctoget
from .utils import fetch
# UTILS
async def info():
    return {
    "project":"simple-scrape-api",
    "note":"This api is made for educational purpouse only. This is just a simple scrapper built arround `Ciarands` vidsrc downloader/resolver.This project was only made to prevent ads and redirects caused by the `iframe`s",
    "version": VERSION,
    "developer":"cool-dev-guy"
    }
