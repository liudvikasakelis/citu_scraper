#!/usr/bin/python3


import l1
import sys

query = sys.argv[2]
site = sys.argv[1]

print(l1.scraper(query, site))

