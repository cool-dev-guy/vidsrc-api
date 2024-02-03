from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # CORS
import requests,asyncio,httpx,gzip
from bs4 import BeautifulSoup
from models import vidsrctoget,vidsrcmeget,upcloudget,vidcloudget,smashyget,info
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get('/')
def index():
    return info()

@app.get('/vidsrc/{dbid}')
async def vidsrc(dbid:str,s:int=None,e:int=None):
    if dbid:
        return await vidsrctoget(dbid,s,e)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid id: {dbid}")

@app.get('/vsrcme/{dbid}')
async def vsrcme(dbid:str = '',s:int=None,e:int=None,l:str='eng'):
    if dbid:
        return await vidsrcmeget(dbid,s,e)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid id: {dbid}")

@app.get("/subs")
async def subs(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        with gzip.open(BytesIO(response.content), 'rt', encoding='utf-8') as f:
            subtitle_content = f.read()

        async def generate():
            yield subtitle_content.encode("utf-8")

        return StreamingResponse(generate(), media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename=subtitle.srt"})

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subtitle: {e}")

    raise HTTPException(status_code=404, detail="Subtitle not found")
