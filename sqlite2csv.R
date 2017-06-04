require(DBI)
require(RSQLite)

intpath = '~/p/citu_scraper/data/work.db'
outpath = '~/p/citu_scraper/data/results1.csv'

mydb <- dbConnect(RSQLite::SQLite(), intpath)

q <- dbReadTable(mydb, 'website')

q <- q[q$website_url != '0',]

write.csv(x=q, file=outpath, row.names=F)

dbDisconnect(mydb)