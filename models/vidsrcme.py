import asyncio
from bs4 import BeautifulSoup
from . import vidsrcpro,superembed
from .utils import fetch
SOURCES = ["VidSrc PRO","Superembed"]
async def get_source(hash:str,url:str):
    SOURCE_REQUEST = await fetch(f"https://vidsrc.stream/rcp/{hash}",headers={"Referer": url})
    try:
        _html = BeautifulSoup(SOURCE_REQUEST.text, "html.parser")
        _encoded = _html.find("div", {"id": "hidden"}).get("data-h") if _html.find("div", {"id": "hidden"}) else None

        if not _encoded:
            return {"stream":None,"subtitle":[]}
        
        _seed = _html.find("body").get("data-i")
        encoded_buffer = bytes.fromhex(_encoded);decoded = ""
        for i in range(len(encoded_buffer)):decoded += chr(encoded_buffer[i] ^ ord(_seed[i % len(_seed)]))
        decoded_url = f"https:{decoded}" if decoded.startswith("//") else decoded
        
        response = await fetch(decoded_url,redirects=False, headers={"Referer": f"https://vidsrc.stream/rcp/{hash}"})
        location = response.headers.get("Location")
        if location is None:
            return {"stream":None,"subtitle":[]}
        if "vidsrc.stream" in location:
            return await vidsrcpro.handle(location,hash,_seed)
        if "multiembed.mov" in location:
            return await superembed.handle(location,hash,_seed)
    except:
        return {"stream":None,"subtitle":[]}

async def get_stream(hash:str,url:str,SOURCE_NAME:str):
    if True:
        RESULT = {}
        RESULT['name'] = SOURCE_NAME
        RESULT['data'] = await get_source(hash,url)
        return RESULT
    else:
        return {"name":SOURCE_NAME,"source":'',"subtitle":[]}

async def get(dbid,s=None,e=None,l='eng'):
    provider = "imdb" if ("tt" in dbid) else "tmdb"
    media = 'tv' if s is not None and e is not None else "movie"
    language = l

    # MAKE API REQUEST TO GET ID(hash)
    id_url = f"https://vidsrc.me/embed/{dbid}" + (f"/{s}-{e}" if s and e else '')
    id_request = await fetch(id_url)
    _html = BeautifulSoup(id_request.text, "html.parser")
    SOURCE_RESULTS = [{"name": attr.text, "hash": attr.get("data-hash")} for attr in _html.find_all("div", {"class": "server"}) if attr.text in SOURCES]

    # REQUEST THE SOURCE
    SOURCE_STREAMS = await asyncio.gather(
        *[get_stream(R.get('hash'),id_url,R.get('name')) for R in SOURCE_RESULTS]
    )
    
    return SOURCE_STREAMS
