import os
import scrapy
import requests
from lxml import html
from scrapy.utils.response import get_base_url
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


class SnapdealDesktopSpider(scrapy.Spider):
    name = "desktops"
    allowed_domains = ["snapdeal.com"]
    
    def start_requests(self):
        urls = [
            'https://www.snapdeal.com/products/computers-desktops?sort=plrty',
        ]
        
        DEFAULT_REQUEST_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                   'Accept-Encoding': 'gzip,deflate','Accept-Language': 'en-US,en;q=0.8,hi;q=0.6,ms;q=0.4',
                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,headers = DEFAULT_REQUEST_HEADERS)
   
    number = 0  
    def parse(self,response):

        

        if self.number>=142:
            os._exit(1)

        DEFAULT_REQUEST_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                   'Accept-Encoding': 'gzip,deflate','Accept-Language': 'en-US,en;q=0.8,hi;q=0.6,ms;q=0.4',
                                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

        url = response.url.split(' ')[-1]

        for a in response.xpath('//div[contains(@class, "col-xs-6 favDp product-tuple-listing js-tuple")]/div[2]/a/@href').extract():

            

            res = requests.get(url = a , headers = DEFAULT_REQUEST_HEADERS)
            tree = html.fromstring(res.content)
            try:
                productName = tree.xpath('.//h1[@class="pdp-e-i-head"]/text()')[0]
            except IndexError:
                pass
            productPrice = tree.xpath('.//span[@class="payBlkBig"]/text()')[0]

            productImageAddresses0 = Selector(text=res.content).xpath('//ul[@class="clearfix  height-inherit"]/li/img/@src').extract()
            productImageAddresses1 = Selector(text=res.content).xpath('//div[@id="bx-pager-left-image-panel"]/a/img/@lazysrc').extract()
            productHighlights = tree.xpath('.//li[@class="col-xs-8 dtls-li"]/span[@class="h-content"]/text()')

            li = Selector(text=res.content).xpath('//div[@class="spec-body specifications"]/div/table/tr/td/table/tr/td/text()').extract()
            i = 0
            productSpecifications = []
            while(i<len(li)):
                key = li[i]
                value = li[i+1]
                productSpecifications.append({key:value},)
                i+=2

            productDescription0 = tree.xpath('.//div[@class="tab-content activeTab"]/div[3]/div[2]/div[@class="detailssubbox"]/text()')
            productDescription1 = tree.xpath('.//div[@class="tab-content activeTab"]/div[3]/div[2]/div[@class="detailssubbox"]/p/text()')
            productDescription2 = tree.xpath('.//div[@class="tab-content activeTab"]/div[3]/div[2]/div[@class="detailssubbox"]/ul/li/text()')
            
            productImageAddresses = productImageAddresses0 + productImageAddresses1
            print productImageAddresses
            
            print productHighlights
            
            print productSpecifications
            productDescription = productDescription0 + productDescription1 + productDescription2

            data = {"desc":productDescription}
            clean_data = ''.join(data['desc'])
            print clean_data.strip(' \r\n\t')

        self.number += 20
        yield scrapy.Request(url="https://www.snapdeal.com/acors/json/product/get/search/55/%d/20?q=&sort=plrty&brandPageUrl=&keyword=&searchState=categoryRedirected=computers-desktops|previousRequest=true|serviceabilityUsed=false|filterState=null&pincode=&vc=&webpageName=categoryPage&campaignId=&brandName=&isMC=false&clickSrc=unknown&showAds=true&cartId=&page=cp" %self.number,callback=self.parse,headers = DEFAULT_REQUEST_HEADERS)
