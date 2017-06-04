#!/usr/bin/python3


import l1
import sys
import random
import time
import pymysql


if len(sys.argv) < 2:
    sys.exit(2)

site = sys.argv[1]

proxy = ''

ret = 0


with pymysql.connect(user='liudvikas', database='citu') as c:
    # c = conn.cursor()
    while True:
        time.sleep(random.gammavariate(1,0.1))
        c.execute('SELECT * FROM citu WHERE website_url = "0" OR website_url = "{}";'.format(list(({'co', 'en'} - {site}))[0]))
        all_names = c.fetchall()
        if len(all_names) == 0:
            break        
        current_name, status = random.choice(all_names)
        ret = l1.scraper(site=site, query=current_name)
        
        if ret in {-1, -2, -4}:
            print(ret)
            break
        
        if ret in {-3, -5}:
            ret = site
            if status != '0':
                ret = "No website"
                
        c.execute('UPDATE citu SET website_url = "{}"'
                  ' WHERE company_name = "{}";'.format(ret, current_name))
        
        c.execute('COMMIT;')
            
            