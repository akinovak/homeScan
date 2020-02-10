import scrapy
import math
import re
import scrapy_splash
from config import ctx
from scrapy_splash import SplashRequest
import datetime


class PolovniAutomobili(scrapy.Spider):

    name = 'polovniautomobili'
    allowed_domains = ['polovniautomobili.com']
    start_urls = [
        'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=1&sort=sort=renewDate_desc&city_distance=0'
        '&showOldNew=all&without_price=1 '
    ]

    def parse(self, response):
        arr_urls = []
        tmpStr = response.css('div.js-hide-on-filter small::text').get()
        numE = int(re.search('Prikazano od 1 do 25 oglasa od ukupno ([0-9]*)', tmpStr).group(1))
        print("OGLASA: " + str(numE))
        numPages = int(math.ceil(numE / 25))

        print("BROJ STRNICA: " + str(numPages))

        for i in range(50):
            url = 'https://www.polovniautomobili.com/auto-oglasi/pretraga?page=' + str(
                i + 1) + '&sort=renewDate_desc&city_distance=0&showOldNew=all&without_price=1'
            arr_urls.append(url)
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_page,
                dont_filter=True
            )

    def parse_page(self, response):
        carUrls = response.css(
            'article.single-classified:not([class*="uk-hidden"]):not([class*="paid-0"]) h2 a::attr(href)').getall()

        carRenewal = response.xpath('//i[has-class("uk-icon-calendar")]/../text()').getall()

        renewal_dates = list(map(lambda x: x.split(':')[1].strip(), carRenewal))

        carUrls = list(map(lambda x: 'https://www.polovniautomobili.com' + x + '?show_date=true', carUrls))
        for (i, url) in enumerate(carUrls, start=0):
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parse_car,
                dont_filter=True,
                meta={'renewal_date': renewal_dates[i]}
            )

    def parse_price(self, obj, response):
        price = response.css('div.price-item::text').get()
        if price == '' or price is None:
            price = response.xpath('//div[has-class("price-item-discount position-relative")]').get()
            price = price.replace('\n', '').replace(' ', '').replace('\t', '')
            price = re.search(r'([0-9]*\.?[0-9]*)€', price).group(1)

        price = price.strip()
        if price == 'Po dogovoru' or price == 'Na upit':
            price = -1
        else:
            first = re.search('([0-9]*)\.?[0-9]*', price)
            second = re.search('[0-9]*\.([0-9]*)', price)
            if second is None:
                price = int(first.group(1))
            else:
                price = int(first.group(1)) * 1000 + int(second.group(1))

        obj['Cena'] = price

    def parse_place(self, obj, response):
        obj['Mesto'] = response.css('aside.table-cell section.uk-grid div div div.uk-width-1-2::text').get().strip()

        if obj['Mesto'] == '':
            obj['Mesto'] = response.css('aside.table-cell section.uk-grid div div div div::text').get().strip()

        if obj['Mesto'] == '':
            obj['Mesto'] = response.css('aside.table-cell section.uk-grid div div::text').get().strip()

        if obj['Mesto'] == '':
            obj['Mesto'] = response.css('aside.table-cell section.uk-grid div div.uk-margin-top-remove div.uk-width-1-2::text').get().strip()

    def parse_car(self, response):
        renewal_date = response.meta.get('renewal_date')
        datetime_object = datetime.datetime.strptime(renewal_date, '%d.%m.%Y.')

        sec = response.css('section.classified-content div div::text').getall()
        o = self._pack_obj(sec, response.request.url, response)

        o = ctx.pa_transformer.transform(o)
        ctx.mongo_repository.handle_object(o, 'polovni')

    def _pack_obj(self, sec, link, response):
        arr = []
        for s in sec:
            w = s.strip()
            if w != '' and '\n' not in w and '\t' not in w:
                arr.append(w)

        features = []
        values = []
        for i in range(len(arr)):
            if i % 2 == 0:
                features.append(arr[i])
            else:
                values.append(arr[i])

        o = {}
        for f, v in zip(features, values):
            if f.strip() in ctx.pa_transform_map:
                o[f.strip()] = v.strip()

        o['Link'] = link
        self.parse_price(o, response)
        self.parse_place(o, response)
        return o
