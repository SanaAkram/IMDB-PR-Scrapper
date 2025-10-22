import scrapy

class IMDbSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/list/ls055386972/'  # URL of the IMDb list
    ]

    def parse(self, response):
        # Loop through each movie in the list
        for movie in response.css('.lister-item'):
            yield {
                'title': movie.css('.lister-item-header a::text').get(),
                'year': movie.css('.lister-item-year::text').get(),
                'rating': movie.css('.ipl-rating-star__rating::text').get(),
                'description': movie.css('.text-muted+ .text-muted::text').get().strip(),
                'runtime': movie.css('.runtime::text').get(),
                'genre': movie.css('.genre::text').get().strip(),
                'director': movie.css('.text-muted~ .text-muted+ p a::text').get(),
            }

        # Handle pagination if available
        next_page = response.css('a.flat-button.lister-page-next.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
