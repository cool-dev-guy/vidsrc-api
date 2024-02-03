# vidsrc-api
`[ PROJECT HAS UNDERGONE VERY LARGE CHANGES IN STRUCTURE AND CONTENT ]`

A simple web scrapper based on this [resolver](https://github.com/Ciarands).

- Please let me know if you are using this code (just for showcasing) :)

- `If you liked it :)`

<a href="https://www.buymeacoffee.com/cooldevguy"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cool-milk&emoji=🥛&slug=cooldevguy&button_colour=222222&font_colour=ffffff&font_family=Lato&outline_colour=ffffff&coffee_colour=FFDD00" /></a>

### FEATURES
```
- async support
- parallel execution
- very fast results
- subtitle support for enery sources.
```
### NOTES
```
- Dont overload the deployment.
- This api is made for educational purpouse only. This is just a simple scrapper built arround `https://github.com/Ciarands` vidsrc downloader.This project was only made to prevent ads and redirects caused by the `iframe`s
- This api isnt a copy of the inspired project,but its a complete reqrite of code to make it work as an api and use async style to give vary fast results.
- Dont perform bulk request to the api and store the m3u8's returned,cuz they may not work after 24 hours or so.This api scrape websites that have `video on demand` feature so storing it is useless.
```
### USAGE (`GET`)
- base url:
  https://api-movie-source.vercel.app

- endpoints:
  - `/vidsrc/{db_id}`
  - `/vsrcme/{db_id}`
  - `/subs/?url={subtitle_url@opensubtitles.org}`

- parameters:
  - `s` - season (series only)
  - `e` - episodes (series only)
  - `l` - language(subtitle)

### RESPONSE SCEMA
> [UPDATE] Added a common response scheam for the endpoints,so every source is an element of an array.And the api retruns an array.


```json
[
  {
    "name": "SOURCE_NAME",
    "data": {
      "file": "FILE.m3u8",
      "sub": "SUBTITLES"
    }
  }
]

```

### ERROR CODES
```
ERROR CODES
===========
1402 : filemoon error.[filemoon domain whitelisting][solution:retry]
1308 : multiembed captcha error.[solution:retry/do captcha]
1309 : vidsrcPro error.[decode error][solution:retry]
1310 : subtitle fetch error.[reload]

1404 : no sources found.
1401 : vidplay error.

1500 : not found error.
500  : internal error/fetch error
```

### OTHER PROJECTS
- [cool-proxy](https://github.com/cool-dev-guy/cool-proxy) - A proxy made in C++
