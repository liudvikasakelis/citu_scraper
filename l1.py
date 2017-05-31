#!/usr/bin/python3

import requests
from lxml import html


def st_scraper(url):
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError:
        return 0
        
    tree = html.fromstring(page.content)
    
    try:
        first = tree.xpath('//a[@class="search-title-link"]/@href')[0]
    except IndexError:
        return 0
    
    try:
        page = requests.get('https://www.companiesintheuk.co.uk' + first)
    except requests.exceptions.ConnectionError:
        return 0
    
    tree = html.fromstring(page.content)
    
    try:
        return(tree.xpath('//strong[contains(text(), "Web")]/following-sibling::a/@href')[0])
    except IndexError:
        return 0


def en_scraper(url):
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError:
        return 0
        
    tree = html.fromstring(page.content)
    
    try:
        first = tree.xpath('//div[@class="search_result"]//a/@href')[0]
    except IndexError:
        return 0
    
    try:
        page = requests.get('https://www.endole.co.uk' + first)
    except requests.exceptions.ConnectionError:
        return 0
    
    tree = html.fromstring(page.content)
    
    try:
        return(tree.xpath('//div[contains(text(), "Website")]/../../td[2]/a/@href')[0])
    except IndexError:
        return 0


def scraper(url, site):
    if site == 'en':
        xpath_query_1 = '//div[@class="search_result"]//a/@href'
        xpath_query_2 = '//div[contains(text(), "Website")]/../../td[2]/a/@href'
        url_prefix = 'https://www.endole.co.uk'
        search_prefix = '/search/?match=companies&search='        
    elif site == 'co':
        xpath_query_1 = '//a[@class="search-title-link"]/@href'
        xpath_query_2 = '//strong[contains(text(), "Web")]/following-sibling::a/@href'
        url_prefix = 'https://www.companiesintheuk.co.uk'
        search_prefix = '/company/find?q='
    else:
        return 'Unknown site id'
    
    try:
        page = requests.get(url_prefix + search_prefix + url)
    except requests.exceptions.ConnectionError:
        return 'Search results not received'
           
    tree = html.fromstring(page.content)
    
    try:
        first = tree.xpath(xpath_query_1)[0]
    except IndexError:
        return '1st result not found in search results'
    
    try:
        page = requests.get(url_prefix + first)
    except requests.exceptions.ConnectionError:
        return 'Company page not received'
    
    tree = html.fromstring(page.content)
    
    try:
        return(tree.xpath(xpath_query_2)[0])
    except IndexError:
        return 'Website URL not found in company page'
    