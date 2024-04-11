import re,base64
from .utils import fetch
from . import subtitle

MAX_TRIES = 10

async def handle(location,hash,_seed):
    request = await fetch(location, headers={"Referer": f"https://vidsrc.stream/rcp/{hash}"})
    for T in range(MAX_TRIES):
        hls_url = re.search(r'file:"([^"]*)"', request.text).group(1)
        hls_url = re.sub(r'\/\/\S+?=', '', hls_url)[2:]     
        hls_url = re.sub(r"\/@#@\/[^=\/]+==", "", hls_url)

        hls_url = hls_url.replace('_', '/').replace('-', '+')
        hls_url = bytearray(base64.b64decode(hls_url))
        hls_url = hls_url.decode('utf-8')
        if hls_url != "" and hls_url.endswith('.m3u8'):  
            break
    # SET PASS
    set_pass = re.search(r'var pass_path = "(.*?)";', request.text).group(1)
    if set_pass.startswith("//"):
        set_pass = f"https:{set_pass}"
    await fetch(set_pass, headers={"Referer": hash})

    subtitles = []
    subtitles = await subtitle.subfetch(_seed,"eng")
    return {"stream":hls_url,"subtitle":subtitles}
    
