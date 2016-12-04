
import requests
import urllib
import json
import re
from bs4 import BeautifulSoup
from urlparse import urlparse
import tldextract
import itertools
import sys
import validators



# this function crawls a page looking for more links to crawl
# takes a set of links and the starting_url as parametrs
def crawl_page(links,first_url):
    # takes a set of links as input
    for link in links:
        url_link = set([])
        #open page and parse html
        page = urllib.urlopen(link).read()
        parsed_html = BeautifulSoup(page,"html.parser")
        #search for links in parsed html
        for link in parsed_html.findAll('a',href=True):
            #get link
            url = link.get('href')
            # match links that start with Http
            match_obj = re.match( '^http', url)
            #check if link is valid
            validate_url = urlparse(url)
            if match_obj != None and bool(validate_url.scheme):
                #extrac domain from link and compare to domain of starting liink
                if tldextract.extract(url).domain == tldextract.extract(first_url).domain:
                    if str(validate_url.netloc)[:4] != 'http':
                        url_string= 'http://'+str(validate_url.netloc)
                        url_link.add( url_string)
                    else:
                        url_link.add(str(validate_url.netloc) )
                else:
                    continue
            #find other links
            elif (url.startswith('/') or url.endswith('.html')) and (not bool(validate_url.scheme)):

                url_link.add( str(first_url +url))
            else:
                continue
    return url_link
# this function stores crawled pages to a certain depth using breadth first search
def crawler_bfs(starting_url,depth):
    #check if url is valid
    try:
        requests.head(starting_url)
    except:
        message = 'Invalid url'
        if True:
            raise Exception(message + ', please input a valid url')

    #initialise queue with first url
    new_url, visited_queue = set([starting_url]),set([starting_url])
    if depth == 0:
        counter =1
    else:
        counter = 0
    while counter <= depth:
        # retrieve crawable links
        page_set = crawl_page(new_url,starting_url)
        new_url.clear()
        new_page = False
        for page in page_set:
             #check if page has been visited
             if page not in visited_queue:
                # if there's a new page add to visited_queue
                new_page = True
                visited_queue.add(page)
                new_url.add(page)
        # if there is a new page continue crawling else stop
        if new_page:
            counter += 1
        else:
            counter = depth+1
    return visited_queue

# this function gets the static files from pages
def get_static_links(url):
    #open page and parse html
    page = urllib.urlopen(url).read()
    parsed_html = BeautifulSoup(page,"html.parser")
    # get static files and store them as a list
    link_images = [str(link['href']) for link in parsed_html.find_all('link', href=re.compile(r'(.*\.(?:jpg|png|jpeg|giff|tiff))'))]
    img = [str(link['src']) for link in parsed_html.find_all('img',src=True)]
    css = [str(link['href']) for link in parsed_html.find_all('link', rel="stylesheet")]
    script = [str(link['src']) for link in parsed_html.findAll('script',src=True)]
    # concatenate lists
    assets = list(itertools.chain(link_images, img, css,script))




    #return dictionary of of url an stati files
    return {'url': url, 'assets': assets}

# print out urls and heir static files.
# take imputs from the command line
if __name__ == '__main__':
    first_url = sys.argv[1]

    if len(sys.argv)>2:

        depth = int(sys.argv[2])
    else:
        depth = 20
    STDOUT = json.dumps([get_static_links(reached_links) for reached_links in crawler_bfs(first_url,depth)],indent=4, separators=(',', ': '))
    print STDOUT
