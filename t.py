#!/usr/bin/python3


import l1
import sys

query = sys.argv[1]

print(l1.st_scraper('https://www.companiesintheuk.co.uk/Company/Find?q=' + query))

print(l1.en_scraper('https://www.endole.co.uk/search/?match=companies&search=' + query))