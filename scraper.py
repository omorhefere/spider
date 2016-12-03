
import requests
import urllib
import json
import re
from StringIO import StringIO
from bs4 import BeautifulSoup
from urlparse import urlparse
import tldextract
import itertools
import time

domain = 'http://www.ooimoloame.co.uk/'


def crawl_page(links):

    for link in links:
        urllink = set([])

        page = urllib.urlopen(link).read()
        parsedHtml = BeautifulSoup(page,"html.parser")

        for link in parsedHtml.findAll('a',href=True):
            uri = link.get('href')
            matchObj = re.match( '^http', uri)
            check_url = urlparse(uri)
            if matchObj != None and bool(check_url.scheme):
                if tldextract.extract(uri).domain == tldextract.extract(domain).domain:
                    if str(check_url.netloc)[:4] != 'http':
                        url_string= 'http://'+str(check_url.netloc)
                        urllink.add( url_string)
                    else:
                        urllink.add(str(check_url.netloc) )
                else:
                    continue
            elif (uri.startswith('/') or uri.endswith('.html')) and (not bool(check_url.scheme)):
                urllink.add( str(domain +uri))
            else:
                continue
    return urllink

def crawler_bfs(starting_url,depth):
    new_url, visited_queue = set([starting_url]),set([starting_url])
    counter = 0
    while counter <= depth:

        page_set = crawl_page(visited_queue)

        new_url.clear()
        new_page = False
        for page in page_set:
             if page not in visited_queue:
                new_page = True
                visited_queue.add(page)
                new_url.add(page)
        if new_page:
            counter += 1
        else:
            counter = depth+1
    return visited_queue


def get_static_links(url):


    page = urllib.urlopen(url).read()
    parsedHtml = BeautifulSoup(page,"html.parser")
    link_images = [str(link['href']) for link in parsedHtml.find_all('link', href=re.compile(r'(.*\.(?:jpg|png|jpeg|giff|tiff))'))]
    img = [str(link['src']) for link in parsedHtml.find_all('img')]
    css = [str(link['href']) for link in parsedHtml.find_all('link', rel="stylesheet")]
    script = [str(link['src']) for link in parsedHtml.findAll('script',src=True)]
    assets = list(itertools.chain(link_images, img, css,script))
    print len(assets)


    return {'url': url, 'assets': assets}

start = time.time()
print("hello")
STDOUT = json.dumps([get_static_links(reached_links) for reached_links in crawler_bfs(domain,2)],indent=4, separators=(',', ': '))
end = time.time()
print(end - start)
