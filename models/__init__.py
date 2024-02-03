from .subtitle import subfetch
VERSION = '1.0.0'
from .upcloud import get as upcloudget
from .vidcloud import get as vidcloudget
from .vidsrcme import get as vidsrcmeget
from .vidsrcto import get as vidsrctoget
from .smashystream import get as smashyget
# UTILS
def info():
    return {
    "project":"simple-scrape-api",
    "note":"This api is made for educational purpouse only. This is just a simple scrapper built arround `Ciarands` vidsrc downloader/resolver.This project was only made to prevent ads and redirects caused by the `iframe`s",
    "version": VERSION,
    "developer":"cool-dev-guy"
    }
