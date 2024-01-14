from typing import Optional
import requests
async def subfetch(code, language) -> Optional[str]:
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

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        best_subtitle = max(response.json(), key=lambda x: x.get('score', 0), default=None)
        if best_subtitle is None:return None
        return best_subtitle.get("SubDownloadLink")
    return 1310
