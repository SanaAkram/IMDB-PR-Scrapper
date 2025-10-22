import scrapy

class IMDbSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/list/ls055386972/'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 10,
        'DOWNLOADER_MIDDLEWARES': {
            'imdb_scraper.middlewares.ForceUTF8Middleware': 543,
        }
    }

    def parse(self, response):
        for movie in response.css('div.ipc-metadata-list-summary-item__c'):
            yield {
                'title': movie.css('h3.ipc-title__text::text').get(),
                'year': movie.css('span.dli-title-metadata-item::text').get(),
                'duration': movie.css('span.dli-title-metadata-item::text').getall()[1],
                'rating': movie.css('span.ipc-rating-star--rating::text').get(),
                'metascore': movie.css('span.metacritic-score-box::text').get(),
                'plot': movie.css('div.ipc-html-content-inner-div::text').get(),
                'director': movie.css('a.dli-director-item::text').get(),
                'stars': movie.css('a.dli-cast-item::text').getall(),
            }

        next_page = response.css('a.flat-button.lister-page-next.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
