import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        for book  in response.css("li > article.product_pod") : 


            yield { 
                "Title":book.css("h3 a::attr(title)").get(), 
                "ImageLink": response.urljoin(book.css("img::attr(src)").get())  , 
                "Price":  book.css("p.price_color::text").get(), 
                "InStock":self.is_instock(book)   , 
                "Rating":  book.css("p.star-rating::attr(class)").get().split()[-1] , 
            }
        next = response.css("li.next a::attr(href)").get()
        if next is not None : 
            yield response.follow(next, callback=self.parse)

    def is_instock(self,book)->bool:
        if book.css("i.icon-ok").get() is not None:
            return True 
        return False 