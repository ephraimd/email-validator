from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import time
import sys

proxy_basket = ""

class badKitten:

    def __init__(self, system_delay):
        '''Startup the worker thread'''
        self.delay = system_delay/3  #half that time to speed things up
        self.loadProxies()
        pass

    def loadProxies(self):
        proxy_basket = "https://free-proxy-list.net/"
        self.response = requests.get(proxy_basket)
        parser = fromstring(self.response.text)
        self.proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                self.proxies.add(proxy)
        if len(self.proxies) == 0:
            print("Failed to Load Proxy List! You need a VPN to acquire proxies!")
            return False
        else:
            return True
        #setup proxies list


    def loadProxiesNew(self):
        proxy_basket = 'http://pubproxy.com/api/proxy?limit=20&format=json&https=true'
        self.response = requests.get(proxy_basket)
        data = self.response.json()
        self.proxies = set()
        for i in data["data"]:
            self.proxies.add(i['ipPort'])
        if len(self.proxies) == 0:
            print("Failed to Load Proxy List! Proxy API gives only 100 per day for free accounts!")
            sys.exit(-1)
        #setup proxies list

    def scratchAPI(self, url, email):
        proxy_pool = cycle(self.proxies)
        for i in range(1,11):
            #Get a proxy from the pool
            proxy = next(proxy_pool)
            print("\t =>Checking using proxy: %s" % proxy)
            try:
                response = requests.get(url+email,proxies={"http": proxy, "https": proxy})
                return response.json()
            except:
                #Most free proxies will often get connection errors. We will have retry the entire request using another proxy to work. 
                print("\t =>Skipping. Using new Proxy; but will wait...")
                time.sleep(self.delay)
                print("\t =>Done waiting,...")
        return False
