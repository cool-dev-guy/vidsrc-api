# VIDSRC.TO
# file made by @cool-dev-guy using @Ciarands resolver to support fastapi.
from urllib.parse import unquote
import httpx,asyncio,base64,requests
from bs4 import BeautifulSoup
from . import vidplay,filemoon,utils
async def vidsrcto(source_id) -> str:
    # SHIT
    MAX_ATTEMPTS = 10
    for i in range(MAX_ATTEMPTS):
        print(i)
        try:
            req = requests.get(f"https://vidsrc.to/ajax/embed/source/{source_id}")
            data = req.json()
            encrypted_source_url = data.get("result", {}).get("url")
            break
        except:
            data = None
            encrypted_source_url = None
            pass
    


    standardized_input = encrypted_source_url.replace('_', '/').replace('-', '+')
    binary_data = base64.b64decode(standardized_input)

    encoded = bytearray(binary_data)

    # SPECIAL [KEY]
    key_bytes = bytes('8z5Ag5wgagfsOuhz', 'utf-8')
    j = 0
    s = bytearray(range(256))

    for i in range(256):
      j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
      s[i], s[j] = s[j], s[i]

    decoded = bytearray(len(encoded))
    i = 0
    k = 0

    for index in range(len(encoded)):
      i = (i + 1) & 0xff
      k = (k + s[i]) & 0xff
      s[i], s[k] = s[k], s[i]
      t = (s[i] + s[k]) & 0xff
      decoded[index] = encoded[index] ^ s[t]

    decoded_text = decoded.decode('utf-8')
    return unquote(decoded_text)

async def get(dbid:str,s:int=None,e:int=None):
    provider = "imdb" if ("tt" in dbid) else "tmdb"
    media = 'tv' if s is not None and e is not None else "movie"
    sources = ['Vidplay','Filemoon']
    url = f"https://vidsrc.to/embed/{media}/{dbid}"
    url += f"/{s}/{e}" if s and e else ''
    async with httpx.AsyncClient() as client:
        #SHITTT cool-dev-guys logic to bypass errors ...
        MAX_ATTEMPTS = 5
        for i in range(MAX_ATTEMPTS):
            try:
                req = await client.get(url)
                soup = BeautifulSoup(req.text, "html.parser")
                sources_code = soup.find('a', {'data-id': True}).get("data-id",None)
                break
            except:
                sources_code = None
                continue
        
        if sources_code == None:return 1404
        req = await client.get(f"https://vidsrc.to/ajax/embed/episode/{sources_code}/sources")
        data = req.json()
        sources = {video.get("title"): video.get("id") for video in data.get("result")}

        filemoon_id = sources.get('Filemoon', None)
        vidplay_id = sources.get('Vidplay', None)
        
        if not filemoon_id and not vidplay_id:
            return 1404
        results = await asyncio.gather(
            vidsrcto(vidplay_id) if vidplay_id else utils.default(),
            vidsrcto(filemoon_id) if filemoon_id else utils.default()
        )
        streams = await asyncio.gather(
            vidplay.handle_vidplay(results[0]) if "55a0716b8c" in results[0] else utils.default(),
            filemoon.handle_filemoon(results[1]) if "keraproxy" in results[1] else utils.default(),
        )
        return [{"name":"Vidplay","data":streams[0]},{"name":"Filemoon","data":streams[1]}]
