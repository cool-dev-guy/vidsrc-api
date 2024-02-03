# API --- filemoon --- vidsrc.to provider
# file made by @cool-dev-guy using @Ciarands vidsrc-to-resolver
import requests
import re
def unpack(p, a, c, k, e=None, d=None) -> str:
    for i in range(c - 1, -1, -1):
      if k[i]: p = re.sub("\\b" + int_2_base(i, a) + "\\b", k[i], p)
    return p
def int_2_base(x: int, base: int) -> str:
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"

    if x < 0:
        sign = -1
    elif x == 0:
        return 0
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(charset[int(x % base)])
        x = int(x / base)
        
    if sign < 0:
        digits.append('-')
    digits.reverse()

    return ''.join(digits)
async def handle_filemoon(url) -> str:
    req = requests.get(url)
    matches = re.search(r'return p}\((.+)\)', req.text)
    
    processed_matches = []
    # these are specific to filemoon(cool lol)
    if not matches:
      for i in range(10):
        req = requests.get(url)
        matches = re.search(r'return p}\((.+)\)', req.text)
        if matches != None:break
    if not matches:
      return 1402
    split_matches = matches.group(1).split(",")
    corrected_split_matches = [",".join(split_matches[:-3])
                               ] + split_matches[-3:]

    for val in corrected_split_matches:
      val = val.strip()
      val = val.replace(".split('|'))", "")
      if val.isdigit() or (val[0] == "-" and val[1:].isdigit()):
        processed_matches.append(int(val))
      elif val[0] == "'" and val[-1] == "'":
        processed_matches.append(val[1:-1])

    processed_matches[-1] = processed_matches[-1].split("|")
    unpacked = unpack(*processed_matches)
    hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
    return {'file':hls_url,
            'sub':1404}
