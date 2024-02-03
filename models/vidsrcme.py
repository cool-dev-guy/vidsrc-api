import requests
import requests,asyncio,httpx
from bs4 import BeautifulSoup
from . import vidsrcpro,superembed
from . import subtitle
async def vidsrcme(source,url):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"https://rcp.vidsrc.me/rcp/{source}",headers={"Referer": url})
        _html = BeautifulSoup(response.text, "html.parser")
        _encoded = _html.find("div", {"id": "hidden"}).get("data-h") if _html.find("div", {"id": "hidden"}) else None
        if not _encoded:return None
        _seed = _html.find("body").get("data-i")

        encoded_buffer = bytes.fromhex(_encoded);decoded = ""
        for i in range(len(encoded_buffer)):decoded += chr(encoded_buffer[i] ^ ord(_seed[i % len(_seed)]))
        decoded_url = f"https:{decoded}" if decoded.startswith("//") else decoded
        
        response = requests.get(decoded_url, allow_redirects=False, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})
        location = response.headers.get("Location")
        if location is None:
            return 1506,_seed
        if "playhydrax.com" in location:
            return 1500,_seed
        if "vidsrc.stream" in location:
            req = await client.get(location, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})
            return await vidsrcpro.handle_vidsrcpro(req,source,_seed)
        if "2embed.cc" in location:
            return 1500,_seed
        if "multiembed.mov" in location:
            return await superembed.handle_superembed(location,source,_seed)
async def get(dbid,s=None,e=None,l='eng'):
    provider = "imdb" if ("tt" in dbid) else "tmdb"
    media = 'tv' if s is not None and e is not None else "movie"
    language = l

    url = f"https://vidsrc.me/embed/{dbid}"
    url += f"/{s}-{e}" if s and e else ''

    response = requests.get(url)
    _html = BeautifulSoup(response.text, "html.parser")
    sources = {attr.text: attr.get("data-hash") for attr in _html.find_all("div", {"class": "server"})}
        
    # REMOVE UNWANTED SOURCES
    try:
        del sources['VidSrc Hydrax']
    except:
        pass
    try:
        del sources['2Embed']
    except:
        pass
    # RESULT SCHEMA
    source = []
    for item in sources.keys():source.append(sources[item])
    if not source:return 1404,None
    results = await asyncio.gather(
        *[vidsrcme(s,url) for s in source]
    )
    print(results)
    sub_seed = results[0][1] if results[0] else 1500
    subtitles = await subtitle.subfetch(sub_seed,language) if sub_seed!=500 else 500
    return [{
    "name":'VidSrcPRO',
    "data":{
            'file':results[0][0],
            'sub':subtitles
        },
    },{
    "name":'SuperEmbed',
    "data":{
            'file':results[1][0] if len(results)==2 else 1500,
            'sub':results[1][1] if len(results)==2 else 1500
        },
    }]
