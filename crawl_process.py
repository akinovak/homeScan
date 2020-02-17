from scrapers.nekretnine_srbija import NekretnineSrbija
from scrapers.polovni_automobili import PolovniAutomobili
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from config import ctx
import sys

print('==================')
print(sys.argv)
print('==================')
print('Crawling started')
s = get_project_settings()
s['USER_AGENTS'] = ctx.user_agents
s['DOWNLOAD_DELAY'] = 0.5
s['DOWNLOADER_MIDDLEWARES'] = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
s['COOKIES_ENABLED'] = True
s['COOKIES_DEBUG'] = True
s['SPLASH_URL'] = 'http://192.168.59.103:8050'

s['SPIDER_MIDDLEWARES'] = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
s['DUPEFILTER_CLASS'] = 'scrapy_splash.SplashAwareDupeFilter'
s['HTTPCACHE_STORAGE'] = 'scrapy_splash.SplashAwareFSCacheStorage'

process = CrawlerProcess(s)
#process.crawl(NekretnineSrbija)
process.crawl(PolovniAutomobili)
process.start()
print('Crawling finished')
