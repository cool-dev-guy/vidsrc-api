from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
import gzip
import base64
import requests
import asyncio
from io import BytesIO
from typing import Optional
from bs4 import BeautifulSoup
import httpx
#from scraper import extractor
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cool-dev-guy.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VERSION = '0.0.1'
@app.get('/')
def hello():
    return {"version": VERSION}
def hunter_def(d, e, f) -> int:
    g = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/");h = g[0:e];i = g[0:f];d = list(d)[::-1];j = 0;k = ""
    for c,b in enumerate(d):
        if b in h:j = j + h.index(b)*e**c
    while j > 0:k = i[j%f] + k;j = (j - (j%f))//f
    return int(k) or 0
def hunter( h, u, n, t, e, r) -> str:
        '''Decodes the common h,u,n,t,e,r packer'''
        r = ""
        i = 0
        while i < len(h):
            j = 0
            s = ""
            while h[i] is not n[e]:
                s = ''.join([s,h[i]])
                i = i + 1

            while j < len(n):
                s = s.replace(n[j],str(j))
                j = j + 1

            r = ''.join([r,''.join(map(chr, [hunter_def(s,e,10) - t]))])
            i = i + 1

        return r
async def subfetch(code, language) -> Optional[str]:
    if "_" in code:
        code, season_episode = code.split("_")
        season, episode = season_episode.split('x')
        url = f"https://rest.opensubtitles.org/search/episode-{episode}/imdbid-{code}/season-{season}/sublanguageid-{language}"
    else:
        url = f"https://rest.opensubtitles.org/search/imdbid-{code}/sublanguageid-{language}"
    headers = {
        'authority': 'rest.opensubtitles.org',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'x-user-agent': 'trailers.to-UA',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        best_subtitle = max(response.json(), key=lambda x: x.get('score', 0), default=None)
        if best_subtitle is None:return None
        return best_subtitle.get("SubDownloadLink")
    return None
async def vidsrcme(source,url):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://rcp.vidsrc.me/rcp/{source}",headers={"Referer": url})
        _html = BeautifulSoup(response.text, "html.parser")
        _encoded = _html.find("div", {"id": "hidden"}).get("data-h")
        _seed = _html.find("body").get("data-i")

        encoded_buffer = bytes.fromhex(_encoded);decoded = ""
        for i in range(len(encoded_buffer)):decoded += chr(encoded_buffer[i] ^ ord(_seed[i % len(_seed)]))
        decoded_url = f"https:{decoded}" if decoded.startswith("//") else decoded

        response = await client.get(decoded_url, follow_redirects=False, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})
        location = response.headers.get("Location")
        if "vidsrc.stream" in location:
            req = await client.get(location, headers={"Referer": f"https://rcp.vidsrc.me/rcp/{source}"})

            hls_url = re.search(r'file:"([^"]*)"', req.text).group(1)
            hls_url = re.sub(r'\/\/\S+?=', '', hls_url).replace('#2', '')
            
            try:
                while not hls_url.endswith('.m3u8'):
                    hls_urlx = base64.b64decode(hls_url).decode('utf-8') # this randomly breaks and doesnt decode properly, will fix later, works most of the time anyway, just re-run
                    print(hls_urlx)
            except Exception:
                print(hls_url)
                return "POSSIBLE ERROR",_seed

            set_pass = re.search(r'var pass_path = "(.*?)";', req.text).group(1)
            if set_pass.startswith("//"):
                set_pass = f"https:{set_pass}"

            requests.get(set_pass, headers={"Referer": source})
            return hls_urlx,_seed
        if "2embed.cc" in location:
            return None,_seed
        if "multiembed.mov" in location:
            '''Fallback site used by vidsrc'''
            req = requests.get(location, headers={"Referer":  f"https://rcp.vidsrc.me/rcp/{source}"})
            matches = re.search(r'escape\(r\)\)}\((.*?)\)', req.text)
            processed_values = []

            if not matches:
                return f"CAPTCHA ERROR ,DO CAPTCHA : {location}",_seed

            for val in matches.group(1).split(','):
                val = val.strip()
                if val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                    processed_values.append(int(val))
                elif val[0] == '"' and val[-1] == '"':
                    processed_values.append(val[1:-1])

            unpacked = hunter(*processed_values)
            hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
            return hls_url,_seed
@app.get('/source/{dbid}')
async def source(dbid:str = '',s:int=None,e:int=None,l:str='eng'):
    if dbid:
        provider = "imdb" if ("tt" in dbid) else "tmdb"
        media = 'tv' if s is not None and e is not None else "movie"
        language = l

        url = f"https://vidsrc.me/embed/{media}?{provider}={dbid}"
        url += f"&season={s}&episode={e}" if s and e else ''

        response = requests.get(url)
        _html = BeautifulSoup(response.text, "html.parser")
        sources = {attr.text: attr.get("data-hash") for attr in _html.find_all("div", {"class": "server"})}

        source = []
        for item in sources.keys():source.append(sources[item])
        if not source:return "SOURCE ERROR",None


        results = await asyncio.gather(
            *[vidsrcme(s,url) for s in source]
        )
        sub_seed = results[0][1]
        subtitle = await subfetch(sub_seed,language)
        print(results)
        return [{'source':list(sources.keys())[i],'url':item[0]} for i,item in enumerate(results) if item],subtitle
    else:
        raise HTTPException(status_code=400, detail=f"Invalid id: {dbid}")
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="{HOST}", port=8000,reload=True)
