# citu_scraper #
### Now really quite good ###

Scraped sites: endole.co.uk ('en') or companiesintheuk.co.uk ('co'). Searches for your query using the site search, only takes exact (case-insensitive) name matches and extracts company webpage url if scraped site provides one. From experience, endole has more of them. Supports proxies and only uses the good ones from whatever list you give it. 

Usage:

* Get your company names into an sqlite3 database. Fields: company_name and website_url (fill the latter one with '0'). Set Journal mode pragma to WAL. 
* optional: get some proxies, put them in an sqlite database (see proxies.db). Initial status should be any positive number; it's a weight in a random choosing of proxie. 
* run scraper: ```./t\ sqlite.py 'en' data.db proxies.db  (proxies optional)```
* If a scraper encounters an unusual response (one that doesn't look like a search results page) it will return either -2 or -4 and quit; this to counter website anti-scraping measures by not filling the database with false negatives.
* Since our scraper quits everytime it encounters a network error, we start it up again. A bash loop may be useful, like so:

```bash
while true; do
  sleep 5
  ./t\ sqlite.py 'co' data.db proxies.db
```
Happy scraping!
