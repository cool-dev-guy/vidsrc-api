# API --- superembed --- vidsrc.me provider
# file made by @cool-dev-guy using @Ciarands hunter extractor/resolver
import re
import requests
from bs4 import BeautifulSoup
import httpx
import base64
from .decoders import hunter
from typing import Optional, Dict, List
def process_hunter_args(hunter_args: str) -> List:
    hunter_args = re.search(r"^\"(.*?)\",(.*?),\"(.*?)\",(.*?),(.*?),(.*?)$", hunter_args)
    processed_matches = list(hunter_args.groups())
    processed_matches[0] = str(processed_matches[0])
    processed_matches[1] = int(processed_matches[1])
    processed_matches[2] = str(processed_matches[2])
    processed_matches[3] = int(processed_matches[3])
    processed_matches[4] = int(processed_matches[4])
    processed_matches[5] = int(processed_matches[5])
    return processed_matches
async def handle_superembed(location,source,_seed):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    req = requests.get(location,headers=headers)
    hunter_args = re.search(r"eval\(function\(h,u,n,t,e,r\).*?}\((.*?)\)\)", req.text)
    processed_values = []
    if not hunter_args:
        return f"1308 {location}",_seed
    processed_hunter_args = process_hunter_args(hunter_args.group(1))
    unpacked = hunter.hunter(*processed_hunter_args)
    subtitles = []
    hls_urls = re.findall(r"file:\"([^\"]*)\"", unpacked)
    subtitle_match = re.search(r"subtitle:\"([^\"]*)\"", unpacked)
    if subtitle_match:
        for subtitle in subtitle_match.group(1).split(","):
            subtitle_data = re.search(r"^\[(.*?)\](.*$)", subtitle)
            if not subtitle_data:
                continue
            subtitles.append({'lang':subtitle_data.group(1),'file':subtitle_data.group(2)})
        # print(subtitles)
    return hls_urls[0],subtitles
