import scrapy

from scraper.items import ScraperItem
import logging 
import json
from bs4 import BeautifulSoup

class BookswagonSpider(scrapy.Spider):
    name = "bookswagon"
    allowed_domains = ["bookswagon.com"]
    start_urls = ["https://bookswagon.com"]

    def start_requests(self):
        headers = {
        'authority': 'www.bookswagon.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,te;q=0.7',
        'content-type': 'application/json; charset=UTF-8',
        'cookie': 'CookiesClear=true; CookiesCurrency=true; CurrencyID=BK/E+cXdpE8=; Currency=WXpO/STZ4/k=; CurrencyFactor=iRDGIvHEyTM=; XECurrencyFactor=iRDGIvHEyTM=; CurrencySymbol=+rwmV5yvtsM=; IPCountry=India; IPCountryCode=IN; PartnerID=1; PartnerGroup=1; PrevCurrencyID=5; SortBy=all; PageLayout=list; MenuTypeUser=Cat',
        'origin': 'https://www.bookswagon.com',
        'referer': 'https://www.bookswagon.com/arts-photography-books',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
      }
        for i in range(100):
            payload = f"""{{"searchTerm": "*:*", "ID_Search": 100000, "next_item_index": "{i}", "filter": "category", "ID_ProductType": 1, "IsAlterQuery": true, "FilterQuery": ""}}"""
            yield scrapy.Request(
                    url = "https://www.bookswagon.com/ajax.aspx/GetCategorySearchResult",
                    method = "POST",
                    headers = headers,
                    body = payload,
                    callback=self.parse_book_urls
                    )
            
    def parse_book_urls(self, response):
        links = []
        data = json.loads(response.text)
        soup = BeautifulSoup(data["d"],"lxml")
        for div in soup.find_all('div', class_='cover'):
            for a in div.find_all('a'):
                links.append(a["href"])

        for url in links:
            headers = {
                'authority': 'www.bookswagon.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,te;q=0.7',
                'cache-control': 'max-age=0',
                'cookie': 'CookiesClear=true; CookiesCurrency=true; CurrencyID=BK/E+cXdpE8=; Currency=WXpO/STZ4/k=; CurrencyFactor=iRDGIvHEyTM=; XECurrencyFactor=iRDGIvHEyTM=; CurrencySymbol=+rwmV5yvtsM=; IPCountry=India; IPCountryCode=IN; ASP.NET_SessionId=5a253vxnjuym314q3x24pqtl; PartnerID=1; PartnerGroup=1; PrevCurrencyID=5; SortBy=all; PageLayout=list; MenuTypeUser=books',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            yield scrapy.Request(
                url = url,
                headers=headers,
                callback=self.parse,
            )


    def parse(self, response):
        book = ScraperItem()
        book["url"] = response.url
        soup = BeautifulSoup(response.text,"lxml")
        detail_div = soup.find("div", class_="product-detailwrapper")
        categories = detail_div.select("div.col-md-12 > a")
        hierarchy = []
        for category in categories:
            hierarchy.append(category.text)
            
        hierarchy = "::".join(hierarchy)
        #print(hierarchy)
        book["category"]= hierarchy

        title = soup.select_one("#ctl00_phBody_ProductDetail_lblTitle").text
        #print(title)
        book["title"] = title

        author = soup.select_one("#ctl00_phBody_ProductDetail_lblAuthor1").a.text
        #print(author)
        book["author"] = author

        price = soup.select_one("#ctl00_phBody_ProductDetail_lblourPrice").text
        #print(len(price))
        book["price"]=price
        key_map = {
            "ISBN-13": "isbn13",
            "ISBN-10": "isbn10",
            "Publisher": "publisher",
            "Height": "height", 
            "No of Pages": "noOfPages",
            "Publisher Date": "publisherDate",
            "Binding": "binding",
            "Language": "language",
            "Width": "width",
            "Depth": "depth",
            "Returnable": "returnable",
            "Sub Title": "subTitle",
            "Weight": "weight",
        }

        detail_div = soup.find("div", id="bookdetail")
        for col in detail_div.find_all("div",class_="col-sm-6"):
            for ul in col.find_all("ul"):
                for li in ul.find_all("li"):
                    key, _, value = li.text.partition(":")
                    if key in key_map:
                        field_name = key_map[key]
                        book[field_name] = value

        yield book
