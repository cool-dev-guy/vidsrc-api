# API --- vidsrc.me --- provider
import requests,re,base64
async def handle_vidsrcpro(req,source,_seed):
    hls_url = re.search(r'file:"([^"]*)"', req.text).group(1)
    hls_url = re.sub(r'\/\/\S+?=', '', hls_url)[2:]
            
    MAX_TRIES = 5
    for i in range(MAX_TRIES):
        hls_url = re.sub(r"\/@#@\/[^=\/]+==", "", hls_url)
        if re.search(r"\/@#@\/[^=\/]+==", hls_url):
            continue
    hls_url = hls_url.replace('_', '/').replace('-', '+')
    hls_url = bytearray(base64.b64decode(hls_url))
    hls_url = hls_url.decode('utf-8')
            
    set_pass = re.search(r'var pass_path = "(.*?)";', req.text).group(1)
    if set_pass.startswith("//"):
        set_pass = f"https:{set_pass}"
    requests.get(set_pass, headers={"Referer": source})
    return (hls_url),_seed
