import requests
from typing import Union
from . import subtitle
import re
import base64
def decode_data(key: str, data: Union[bytearray, str]) -> bytearray:
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
async def handle_vidplay(url) -> str:
    furl = url
    url = url.split("?")
    # SUBS = url[1]
    subtitles = {}
    subtitles = await subtitle.vscsubs(url[1])
    key1, key2 = requests.get(
        'https://raw.githubusercontent.com/Ciarands/vidsrc-keys/main/keys.json'
    ).json()
    decoded_id = decode_data(key1, url[0].split('/e/')[-1])
    encoded_result = decode_data(key2, decoded_id)
    encoded_base64 = base64.b64encode(encoded_result)
    key = encoded_base64.decode('utf-8').replace('/', '_')

    req = requests.get("https://vidplay.online/futoken", {"Referer": url})
    fu_key = re.search(r"var\s+k\s*=\s*'([^']+)'", req.text).group(1)
    data = f"{fu_key},{','.join([str(ord(fu_key[i % len(fu_key)]) + ord(key[i])) for i in range(len(key))])}"
    
    req = requests.get(
        f"https://vidplay.online/mediainfo/{data}?{url[1]}&autostart=true",
        headers={"Referer": furl})
    req_data = req.json()
    if type(req_data.get("result")) == dict:
      return {'file':req_data.get("result").get("sources", [{}])[0].get("file"),
              'sub':subtitles}
    return 1401
