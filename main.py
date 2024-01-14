from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import asyncio
from bs4 import BeautifulSoup
import httpx
import models

app = FastAPI()
# API ----- default route
VERSION = '1.0.0'
@app.get('/')
def hello():
    return {
        "project":"simple-scrape-api",
        "note":"This api is made for educational purpouse only. This is just a simple scrapper built arround `https://github.com/Ciarands` vidsrc downloader.This project was only made to prevent ads and redirects caused by the `iframe`s",
        "version": VERSION,
        "developer":"https://github.com/cool-dev-guy"
        }

# API ----- vidsrc.to
@app.get('/extra/{dbid}')
async def additional(dbid:str,s:int=None,e:int=None):
    if dbid:
        provider = "imdb" if ("tt" in dbid) else "tmdb"
        media = 'tv' if s is not None and e is not None else "movie"
        sources = ['Vidplay','Filemoon']
        url = f"https://vidsrc.to/embed/{media}/{dbid}"
        url += f"/{s}/{e}" if s and e else ''
        async with httpx.AsyncClient() as client:
          req = await client.get(url)
          soup = BeautifulSoup(req.text, "html.parser")

          sources_code = soup.find('a', {'data-id': True}).get("data-id")
          req = await client.get(f"https://vidsrc.to/ajax/embed/episode/{sources_code}/sources")
          data = req.json()

          sources = {video.get("title"): video.get("id") for video in data.get("result")}

          filemoon_id = sources['Filemoon'] if sources['Filemoon'] != None else None
          vidplay_id = sources['Vidplay'] if sources['Vidplay'] != None else None
          if not filemoon_id and not vidplay_id:
            return 1404
          results = await asyncio.gather(
              models.vidsrcto(vidplay_id),
              models.vidsrcto(filemoon_id)
          )
          streams = await asyncio.gather(
              models.handle_vidplay(results[0]) if "vidplay" in results[0] else (),
              models.handle_filemoon(results[1]) if "filemoon" in results[1] else (),
          )
          return {"sources":[{"Vidplay":streams[0]},{"Filemoon":streams[1]}]}
    else:
        raise HTTPException(status_code=400, detail=f"Invalid id: {dbid}")
    
# API ----- vidsrc.me
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
        if not source:return 1404,None


        results = await asyncio.gather(
            *[models.vidsrcme(s,url) for s in source]
        )
        sub_seed = results[0][1]
        subtitle = await models.subfetch(sub_seed,language)
        return {'streams':[{'source':list(sources.keys())[i],'url':item[0]} for i,item in enumerate(results) if item],'subtitle':subtitle}
    else:
        raise HTTPException(status_code=400, detail=f"Invalid id: {dbid}")
