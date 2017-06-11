#!/usr/bin/python3


import l1
import sys
import sqlite3
import random
import time
import itertools
import bisect

def weighted_random(elements, weights):
    cumulative_dist = list(itertools.accumulate(weights))
    x = random.random() * cumulative_dist[-1]
    return elements[bisect.bisect(cumulative_dist, x)]

if len(sys.argv) < 3:
    sys.exit(2)

db_path = sys.argv[2]
site = sys.argv[1]

print('Start at {}'.format(time.asctime()))

if len(sys.argv) > 3:
    proxy_file = sys.argv[3]
    with sqlite3.connect(proxy_file) as p:
        c = p.cursor()
        
        c.execute('SELECT http, https FROM proxies')
        proxy_list = c.fetchall()
        
        c.execute('SELECT status FROM proxies;')
        weights = [item for sublist in c.fetchall()for item in sublist]
        
        proxy = weighted_random(proxy_list, weights)
        proxy = {'http':'http://'+proxy[0],
                 'https':'https://'+proxy[1]}
        
    print('Using proxy {}'.format(proxy))
else:
    proxy = {}



ret = 0

with sqlite3.connect(db_path) as conn:
    c = conn.cursor()
    count = 0
    while True:
        time.sleep(random.gammavariate(1, 0.1))
        c.execute('SELECT * FROM website WHERE website_url = "0" OR website_url = ?;',
                  tuple({'co', 'en'} - {site}))
        all_names = c.fetchall()
        if len(all_names) == 0:
            break        
        
        current_name, status = random.choice(all_names)
        
        ret = l1.scraper(site=site, query=current_name, proxies=proxy)
        
        if ret in {-1, -2, -4}:
            print(ret)
            break
        
        if ret in {-3, -5}:
            ret = site
            if status != '0':
                ret = "No website"
                
        c.execute('UPDATE website SET website_url = ? WHERE company_name = ?',
                  [ret, current_name])
        count = count + 1
        
        conn.commit()
        
if proxy:
    with sqlite3.connect(proxy_file) as p:
        c = p.cursor()
        c.execute('SELECT status FROM proxies WHERE http = ?', 
                  [proxy['http'][7:]])
        status = c.fetchone()[0]
        if count == 0:
            status = status * 0.9 + 0.3
        else:
            status = status * 0.95 + count
        c.execute('UPDATE proxies SET status = ? WHERE http = ?', 
                  [status, proxy['http'][7:]])
        
print('Finish at {}'.format(time.asctime()))     
