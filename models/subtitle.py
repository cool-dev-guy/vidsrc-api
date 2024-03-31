# CUSTOM utility FUNCTIONS FOR SUBTITLE MANAGEMENT.
from typing import Optional
from .utils import fetch,BASE
from urllib.parse import unquote
import re
async def subfetch(code, language) -> Optional[str]:
    sub_base_url = f"{BASE}/subs?url="
    if "_" in code:
        code, season_episode = code.split("_")
        season, episode = season_episode.split('x')
        url = f"https://rest.opensubtitles.org/search/episode-{episode}/imdbid-{code}/season-{season}/sublanguageid-{language}"
    else:
        url = f"https://rest.opensubtitles.org/search/imdbid-{code}/sublanguageid-{language}"
    headers = {
        'authority': 'rest.opensubtitles.org',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'x-user-agent': 'trailers.to-UA',
    }

    response = await fetch(url, headers=headers)
    if response.status_code == 200:
        best_subtitle = max(response.json(), key=lambda x: x.get('score', 0), default=None)
        if best_subtitle is None:return None
        return [{"lang":str(language),"file":f"{sub_base_url}{best_subtitle.get('SubDownloadLink')}"}]
    return 1310
async def vscsubs(url):
    subtitles_url = re.search(r"info=([^&]+)", url)
    if not subtitles_url:
        return {}
    
    subtitles_url_formatted = unquote(subtitles_url.group(1))
    MAX_ATTEMPTS = 10
    for i in range(MAX_ATTEMPTS):
        try:
            req = await fetch(subtitles_url_formatted)
                
            if req.status_code == 200:
                return [{"lang":subtitle.get("label"),"file":subtitle.get("file")} for subtitle in req.json()]
        except:
            continue
    return 1310
# file made by @cool-dev-guy
