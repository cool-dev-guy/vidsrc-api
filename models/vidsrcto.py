import asyncio
from bs4 import BeautifulSoup
from . import vidplay,filemoon
from .utils import fetch,error,decode_url

VIDSRC_KEY:str = "WXrUARXb1aDLaZjI"
SOURCES:list = ['Vidplay','Filemoon']

async def get_source(source_id:str,SOURCE_NAME:str) -> str:
    api_request:str = await fetch(f"https://vidsrc.to/ajax/embed/source/{source_id}")
    if api_request.status_code == 200:
        try:
            data:dict = api_request.json()
            encrypted_source_url = data.get("result", {}).get("url")

            return {"decoded":await decode_url(encrypted_source_url,VIDSRC_KEY),"title":SOURCE_NAME}
        except:
            return {}
    else:
        return {}
        
async def get_stream(source_url:str,SOURCE_NAME:str):
    RESULT = {}
    RESULT['name'] = SOURCE_NAME
    if SOURCE_NAME==SOURCES[0]:
        RESULT['data'] = await vidplay.handle(source_url)
        return RESULT
    elif SOURCE_NAME==SOURCES[1]:
        RESULT['data'] = await filemoon.handle(source_url)
        return RESULT
    else:
        return {"name":SOURCE_NAME,"source":'',"subtitle":[]}

async def get(dbid:str,s:int=None,e:int=None):
    media = 'tv' if s is not None and e is not None else "movie"
    id_url = f"https://vidsrc.to/embed/{media}/{dbid}" + (f"/{s}/{e}" if s and e else '')
    id_request = await fetch(id_url)
    if id_request.status_code == 200:
        try:
            soup = BeautifulSoup(id_request.text, "html.parser")
            sources_code = soup.find('a', {'data-id': True}).get("data-id",None)
            if sources_code == None:
                return await error("media unavailable.")
            else:
                source_id_request = await fetch(f"https://vidsrc.to/ajax/embed/episode/{sources_code}/sources")
                source_id = source_id_request.json()['result']
                SOURCE_RESULTS = []
                for source in source_id:
                    if source.get('title') in SOURCES:
                        SOURCE_RESULTS.append({'id':source.get('id'),'title':source.get('title')})

                SOURCE_URLS = await asyncio.gather(
                    *[get_source(R.get('id'),R.get('title')) for R in SOURCE_RESULTS]
                )
                SOURCE_STREAMS = await asyncio.gather(
                    *[get_stream(R.get('decoded'),R.get('title')) for R in SOURCE_URLS]
                )
                return SOURCE_STREAMS
        except:
            return await error("backend id not working.")
    else:
        return await error(f"backend not working.[{id_request.status_code}]")
