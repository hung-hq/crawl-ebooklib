import scrapy
from datetime import datetime
import random

# class test():
#     def test():
#         total_pages = '1 /995563561'
#         index = total_pages.find('/')
#         total_pages = int(total_pages[index+1:])
#         print(total_pages)
# test.test()
class ThuvienpdfSpiderSpider(scrapy.Spider):
    name = "thuvienpdf_spider"
    allowed_domains = ["thuvienpdf.com"]
    start_urls = ["https://thuvienpdf.com/kho-sach/0"]

    with open('user-agent-list.txt', 'r') as file:
        user_agent_list = file.readlines()
 
    def parse(self, response):
        user_agent = random.choice(self.user_agent_list)
        response.headers['User-Agent'] = user_agent

        books = response.css('div.product-cart-wrap')

        for book in books:
            yield {
                'title': book.css('h2 a::text').get(),
                'author': book.css('div.product-price a::text').get(),
                'category': [
                    book.css('div.product-category a::text').get(), 
                    book.css('div.product-badges span::text').get()
                ],
                'url': book.css('div.product-img a::attr(href)').get(),
                'crawl_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

        total_pages = response.css('div.totall-product p .text-brand::text').get()
        index = total_pages.find('/')
        total_pages = int(total_pages[index+1:])

        visited = [False] * total_pages
        for i in range(1, total_pages-1):
            while True:
                index = random.randint(1, total_pages-1)
                if not visited[index]:
                    break
            visited[index] = True
            next_page = f"https://www.thuvienpdf.com/kho-sach/{index}"
            yield scrapy.Request(next_page, callback=self.parse)
