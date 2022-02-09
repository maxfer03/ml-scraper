# MercadoLibre Scraper
A web scraper I'm working on to get data quickly from MercadoLibre.

It currently only works for the "Ropa" category (apparell), but I intend on make it as versatile as possible.

## Instructions
I'm still looking at how to bundle the proyect so that it comes with the required external libraries by default, but for now, you will need to install these packages to run the script:
* openpyxl
* bs4
* requests
* lxml

Tu run the script:
`python3 ml.py [...]`

You can pass as many arguments as you want, but sentences must have hyphens, not spaces!
E.g.:
```
python3 ml.py remera-verde camisa-manga-corta ....
```
