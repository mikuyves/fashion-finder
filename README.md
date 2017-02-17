## SETTINGS BEFORE USE
### Define BASEPATH which is your own work path.

* Define your own BASEPATH in `eshop/eshop/utils/dealitem.py` and `flickr/upload.py`.
```Python
# Define your own BASEPATH which is a ABS-PATH for saving the data.
from secret import BASEPATH
```

* Define your own `api_key` and `api_secret` in `flickr/upload.py`.
```Python
# Define your own BASEPATH which is the same path as scrapy project.
# Get your own api_key and api_secret from https://www.flickr.com/services/api/.
from secret import BASEPATH, api_key, api_secret
```

* Make a file in the project path to record the urls that you need to crape:
```
fashion-finder$ touch urls.txt
```

## SCRAPY

1. Put your urls in your urls.txt file, one url in one line.
2. Start and have fun.
```
fashion-finder$ cd eshop/eshop/spiders/
eshop$ python main_spider.py
```

## FLICKR
`flickr` is a module for me to save the data in cloud, you could skip it if you don't want to.

### Upload
```
fashion-finder$ cd flickr
flickr$ python upload.py
```

### Clean Photoset
```
flickr$ python
-------------------------------
>>> from upload import Myflickr
>>> f = Myflickr()
>>> f.new_photoset()
```


## WEBSITE RULES ADDED

|                Websites | Status                 |
|-------------------------|------------------------|
| www.lanecrawford.com | Some problem with two languages. |
| www.net-a-porter.com | OK. |
| www.farfetch.com | OK. |
| www.shopbop.com | OK. |
| www.mytheresa.com | OK. |
| us.burberry.com | OK. |
| www.luisaviaroma.com | OK. |
| www.matchesfashion.com | OK. |
| www.ssense.com | OK. |
| www.lyst.com | OK. |
| www.shopsplash.com | OK. |
| www.stellamccartney.com | OK. |
| www.neimanmarcus.com | If you try more, it will lead to CAPTCHA. |
| www.fwrd.com | OK. |
| www.madstyle.com.au | OK. |
| www.theoutnet.com | OK. |
| www.armani.com | OK. |
| us.zimmermannwear.com | OK. |
| www.stylebop.com | OK. |
| www.tedbaker.com | OK. |
| www.kenzo.com | Can not scrapy all colors in the same page. |
| cn.sportmax.com | OK. |
| www.melijoe.com | OK. |
| www.modaoperandi.com | OK. |
| www.fashionbarnshop.com | OK. |
| www.amazon.com | It will get 2 sizes of 1 picture. |
