# vidsrc-api
A simple web scrapper based on this [resolver](https://github.com/Ciarands).

<a href="https://www.buymeacoffee.com/cooldevguy"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cool-milk&emoji=🥛&slug=cooldevguy&button_colour=222222&font_colour=ffffff&font_family=Lato&outline_colour=ffffff&coffee_colour=FFDD00" /></a>

### FEATURES
```
- async support
- parallel execution
- very fast results
- subtitle support
```
### NOTES
```
- Dont overload the deployment.
- This api is made for educational purpouse only. This is just a simple scrapper built arround `https://github.com/Ciarands` vidsrc downloader.This project was only made to prevent ads and redirects caused by the `iframe`s
- This api isnt a copy of the inspired project,but its a complete reqrite of code to make it work as an api and use async style to give vary fast results.
```
### USAGE (`GET`)
- base url:
  https://vidsrc-api-five.vercel.app

- endpoints:
  - `/source/{db_id}`
  - `/extra/{db_id}`

- parameters:
  - `s` - season (series only)
  - `e` - episodes (series only)
  - `l` - language(subtitle)

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
```
