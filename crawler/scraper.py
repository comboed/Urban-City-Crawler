from . import crawler
from . import captcha
import requests

class Scraper:
    def __init__(self, captcha_key, max_crawlers, proxy = None):
        self.crawler = crawler.Crawler(max_crawlers, captcha.Captcha(captcha_key), proxy)

    def lookup_query(self, query, page, limit):
        for _ in range(10): # This is not the user's fault and can be many factors, setting to 10 maybe too low?
            random_crawler: requests.Session = self.crawler.get_random_crawler()
            response = random_crawler.get("https://www.google.com/search?q=" + query + "&start=" + str(page - 1)).text

            if ("SPDX-License-Identifier: Apache-2.0" in response):
                self.crawler.crawlers.remove(random_crawler) # Delete this fault crawler
                continue
            
            if ('"WEB_RESULT_INNER",["' not in response):
                continue

            return self.parse_query_data(response, limit)
    
    def parse_query_data(self, data, limit):
        results = {}

        for section in data.split('"WEB_RESULT_INNER",null,"BLUR",0,0,0,null,"')[1:]:
            parts = section.split('"],["')
            
            if (len(parts) < 2):
                continue
        
            results[parts[0]] = parts[1].split('","data:image')[0]

            if (len(results) == limit):
                break

        return results