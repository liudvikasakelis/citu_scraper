#!/usr/bin/python3

import requests
from lxml import html

def scraper(query, site, proxies={}):
    if site == 'en':
        xpath_query_1 = '//div[@class="search_result"]//a[text()="{}"]/@href'.format(query)
        xpath_query_2 = '//div[contains(text(), "Website")]/../../td[2]/a/@href'
        url_prefix = 'https://www.endole.co.uk'
        search_prefix = '/search/?match=companies&search=' 
        xpath_confirmation = '//td/text()'
        text_confirmation = 'COMPANY INSIGHTS'
        xpath_names = '//div[@class="search_result"]//a/text()'
        xpath_url = '//div[@class="search_result"]//a/@href'
    elif site == 'co':
        xpath_query_1 = '//a[@class="search-title-link"]/@href'
        xpath_query_2 = '//strong[contains(text(), "Web")]/following-sibling::a/@href'
        url_prefix = 'https://www.companiesintheuk.co.uk'
        search_prefix = '/company/find?q='
        xpath_confirmation = '//div[@class="searchResult"]/div/@class'
        text_confirmation = 'search_result_title'
        xpath_names = '//div[@class="search_result_title"]/a/text()'
        xpath_url = '//div[@class="search_result_title"]/a/@href'
    else:
        return -1      # unknown site ID
    
    try:
        page = requests.get(url_prefix + search_prefix + query, 
                            proxies=proxies)
    except requests.exceptions.ConnectionError:
        return -2      # search results not received
           
    tree = html.fromstring(page.content)
    
    if text_confirmation not in tree.xpath(xpath_confirmation):
        return -2
    
    search_result_names = tree.xpath(xpath_names)
    first = ''
    for i in range(len(search_result_names)):
        if search_result_names[i].casefold() == query.casefold():
            first = tree.xpath(xpath_url)[i]
    
    if not first:
        return -3
       
    try:
        page = requests.get(url_prefix + first, 
                            proxies=proxies)
    except requests.exceptions.ConnectionError:
        return -4      # Company page not received
    
    tree = html.fromstring(page.content)
    
    try:
        return(tree.xpath(xpath_query_2)[0])
    except IndexError:
        return -5       # Website URL not found in company page
    