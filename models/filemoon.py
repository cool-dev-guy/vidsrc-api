from .utils import fetch
import re
from .decoders.packed import *
from . import subtitle
async def handle(url) -> dict:
    URL = url.split("?")
    SRC_URL = URL[0]
    SUB_URL = URL[1]

    # GET SUB
    subtitles = []
    subtitles = await subtitle.vscsubs(SUB_URL)

	# GET SRC
    request = await fetch(url)
    processed_matches = await process_packed_args(request.text)
    unpacked = await unpack(*processed_matches)
    hls_url = re.search(r'file:"([^"]*)"', unpacked).group(1)
    return {
        'stream':hls_url,
        'subtitle':subtitles
    }
