# API --- vidsrc.me
import re
import requests
from bs4 import BeautifulSoup
import httpx
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
            attempt = 0
            max_try = 5 # SET ANY VALUE
            for i in range(max_try):
                try:
                    req = requests.post("https://www.base64decode.org/",data={
                        'input': f'{hls_url}',
                        'charset': 'UTF-8',
                    })
                    hls_url = BeautifulSoup(req.text,'html.parser').find('textarea',id='output').get_text()
                    if 'm3u8' not in hls_url:
                        continue
                    else:
                        return hls_url,_seed
                except:
                    return 1309,_seed
            # set_pass = re.search(r'var pass_path = "(.*?)";', req.text).group(1)
            # if set_pass.startswith("//"):
            #     set_pass = f"https:{set_pass}"

            # requests.get(set_pass, headers={"Referer": source})
            return hls_url,_seed
        if "2embed.cc" in location:
            return 1500,_seed
        if "multiembed.mov" in location:
            '''Fallback site used by vidsrc'''
            req = requests.get(location, headers={"Referer":  f"https://rcp.vidsrc.me/rcp/{source}"})
            matches = re.search(r'escape\(r\)\)}\((.*?)\)', req.text)
            processed_values = []

            if not matches:
                return f"1308 {location}",_seed

            for val in matches.group(1).split(','):
                val = val.strip()
                if val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                    processed_values.append(int(val))
                elif val[0] == '"' and val[-1] == '"':
                    processed_values.append(val[1:-1])

            unpacked = hunter(*processed_values)
            hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
            return hls_url,_seed
