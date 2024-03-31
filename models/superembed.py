import re
from .utils import fetch
from .decoders.hunter import *

async def handle(location:str,hash:str,_seed:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    request = await fetch(location,headers=headers)
    hunter_args = re.search(r"eval\(function\(h,u,n,t,e,r\).*?}\((.*?)\)\)", request.text)
    if not hunter_args:
        return {"stream":'',"subtitle":[]}
    
    processed_hunter_args = await process_hunter_args(hunter_args.group(1))
    unpacked = await hunter(*processed_hunter_args)
    subtitles = []
    hls_urls = re.findall(r"file:\"([^\"]*)\"", unpacked)
    subtitle_match = re.search(r"subtitle:\"([^\"]*)\"", unpacked)
    if subtitle_match:
        for subtitle in subtitle_match.group(1).split(","):
            subtitle_data = re.search(r"^\[(.*?)\](.*$)", subtitle)
            if not subtitle_data:
                continue
            subtitles.append({'lang':subtitle_data.group(1),'file':subtitle_data.group(2)})
    return {"stream":hls_urls[0],"subtitle":subtitles}
