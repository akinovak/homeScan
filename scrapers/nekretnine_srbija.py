import scrapy
from config import ctx


class NekretnineSrbija(scrapy.Spider):
    name = 'nekretnine_srbija'
    allowed_domains = ['srbija-nekretnine.org']
    start_urls = [
        'https://www.srbija-nekretnine.org/stambeni-objekti/za-izdavanje/beograd?page=1']



    def parse(self, response):
        links = response.xpath("//h3[contains(@class, 'property__title')]/a/@href").getall()
        links = [link.strip()[:link.strip().rfind('?')] for link in links]

        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_page
            )

    def parse_page(self, response):
        features = response.xpath("//dl[contains(@class, 'sn-property__attributes')]/dt/text()").getall()
        values = response.xpath("//dl[contains(@class, 'sn-property__attributes')]/dd/text()").getall()
        o = self._pack_obj(features, values, response.request.url)
        o = ctx.sn_transformer.transform(o)
        ctx.mongo_repository.handle_object(o, 'stanovi')

    def _pack_obj(self, features, values, link):
        o = {}
        if len(values) > len(features):
            values[2] = values[0]
            values.pop(0)
            values.pop(0)
        for f, v in zip(features, values):
            o[f.strip()] = v.strip()
        o['Link'] = link
        return o
