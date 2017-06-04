#!/usr/bin/python3


import l1
import sys
import sqlite3
import random
import time


if len(sys.argv) < 3:
    sys.exit(2)

db_path = sys.argv[2]
site = sys.argv[1]

print('Start at {}'.format(time.asctime()))

if len(sys.argv) > 3:
    proxy_file = sys.argv[3]
    with open(proxy_file, 'r') as f:
        proxy_list = f.read().split()
    proxy = {'https':random.choice(proxy_list)}
    print('Using proxy {}'.format(proxy['https']))
else:
    proxy = {}



ret = 0

with sqlite3.connect(db_path) as conn:
    c = conn.cursor()
    while True:
        time.sleep(random.gammavariate(1,0.1))
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
        
        conn.commit()
       
print('Finish at {}'.format(time.asctime()))     
            
