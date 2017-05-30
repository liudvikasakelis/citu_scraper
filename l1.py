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