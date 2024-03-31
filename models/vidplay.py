from .utils import fetch
from typing import Union
from . import subtitle
import re
import base64
async def decode_data(key: str, data: Union[bytearray, str]) -> bytearray:
    key_bytes = bytes(key, 'utf-8')
    s = bytearray(range(256))
    j = 0

    for i in range(256):
        j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
        s[i], s[j] = s[j], s[i]

    decoded = bytearray(len(data))
    i = 0
    k = 0

    for index in range(len(data)):
        i = (i + 1) & 0xff
        k = (k + s[i]) & 0xff
        s[i], s[k] = s[k], s[i]
        t = (s[i] + s[k]) & 0xff

        if isinstance(data[index], str):
            decoded[index] = ord(data[index]) ^ s[t]
        elif isinstance(data[index], int):
            decoded[index] = data[index] ^ s[t]
        else:
            return None

    return decoded
async def handle(url) -> dict:
    URL = url.split("?")
    SRC_URL = URL[0]
    SUB_URL = URL[1]

    # GET SUB
    subtitles = {}
    subtitles = await subtitle.vscsubs(SUB_URL)

    # DECODE SRC
    key_req        = await fetch('https://raw.githubusercontent.com/Ciarands/vidsrc-keys/main/keys.json')
    key1,key2      = key_req.json()
    decoded_id     = await decode_data(key1, SRC_URL.split('/e/')[-1])
    encoded_result = await decode_data(key2, decoded_id)
    encoded_base64 = base64.b64encode(encoded_result)
    key            = encoded_base64.decode('utf-8').replace('/', '_')

    # GET FUTOKEN
    req = await fetch("https://vidplay.online/futoken", {"Referer": url})
    fu_key = re.search(r"var\s+k\s*=\s*'([^']+)'", req.text).group(1)
    data = f"{fu_key},{','.join([str(ord(fu_key[i % len(fu_key)]) + ord(key[i])) for i in range(len(key))])}"
    
    # GET SRC
    req = await fetch(f"https://vidplay.online/mediainfo/{data}?{SUB_URL}&autostart=true",headers={"Referer": url})
    req_data = req.json()

    # RETURN IT
    if type(req_data.get("result")) == dict:
        return {
            'stream':req_data.get("result").get("sources", [{}])[0].get("file"),
            'subtitle':subtitles
        }
    else:
        return {}
