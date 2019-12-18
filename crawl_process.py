from scrapers.nekretnine_srbija import NekretnineSrbija
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
s['DOWNLOAD_DELAY'] = 0.25
s['DOWNLOADER_MIDDLEWARES'] = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
}

process = CrawlerProcess(s)
process.crawl(NekretnineSrbija)
process.start()
print('Crawling finished')
