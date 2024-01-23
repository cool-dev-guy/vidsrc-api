import re
import requests
import base64
from urllib.parse import unquote
def int_2_base(x, base) -> str:
    charset = list(
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/")

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
def unpack(p, a, c, k, e=None, d=None) -> str:
    for i in range(c - 1, -1, -1):
      if k[i]: p = re.sub("\\b" + int_2_base(i, a) + "\\b", k[i], p)
    return p
def key_permutation(key, data) -> str:
    state = list(range(256))
    index_1 = 0

    for i in range(256):
      index_1 = ((index_1 + state[i]) + ord(key[i % len(key)])) % 256
      state[i], state[index_1] = state[index_1], state[i]

    index_1 = index_2 = 0
    final_key = ''

    for char in range(len(data)):
      index_1 = (index_1 + 1) % 256
      index_2 = (index_2 + state[index_1]) % 256
      state[index_1], state[index_2] = state[index_2], state[index_1]

      if isinstance(data[char], str):
        final_key += chr(
            ord(data[char]) ^ state[(state[index_1] + state[index_2]) % 256])
      elif isinstance(data[char], int):
        final_key += chr((data[char])
                         ^ state[(state[index_1] + state[index_2]) % 256])
    return final_key
async def handle_vidplay(url) -> str:
    key1, key2 = requests.get(
        # KEY PROVIDERS
        # 'https://raw.githubusercontent.com/Claudemirovsky/worstsource-keys/keys/keys.json'
        # 'https://raw.githubusercontent.com/rawgimaster/vidsrc-keys/main/keys.json'
        'https://raw.githubusercontent.com/Ciarands/vidsrc-keys/main/keys.json'
    ).json()  # love u claude
    decoded_id = key_permutation(key1, url.split('/e/')[1].split('?')[0]).encode('Latin_1')
    encoded_result = key_permutation(key2, decoded_id).encode('Latin_1')
    encoded_base64 = base64.b64encode(encoded_result)
    key = encoded_base64.decode('utf-8').replace('/', '_')

    req = requests.get("https://vidplay.site/futoken", {"Referer": url})
    fu_key = re.search(r"var\s+k\s*=\s*'([^']+)'", req.text).group(1)
    data = f"{fu_key},{','.join([str(ord(fu_key[i % len(fu_key)]) + ord(key[i])) for i in range(len(key))])}"
    
    req = requests.get(
        f"https://vidplay.site/mediainfo/{data}?{url.split('?')[1]}&autostart=true",
        headers={"Referer": url})
    req_data = req.json()

    if type(req_data.get("result")) == dict:
      return req_data.get("result").get("sources", [{}])[0].get("file")
    return 1401
async def handle_filemoon(url) -> str:
    req = requests.get(url)
    matches = re.search(r'return p}\((.+)\)', req.text)
    processed_matches = []

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
    return hls_url

async def vidsrcto(source_id) -> str:
    req = requests.get(f"https://vidsrc.to/ajax/embed/source/{source_id}")
    data = req.json()
    encrypted_source_url = data.get("result", {}).get("url")


    standardized_input = encrypted_source_url.replace('_', '/').replace('-', '+')
    binary_data = base64.b64decode(standardized_input)

    encoded = bytearray(binary_data)


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
