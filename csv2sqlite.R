#!/usr/bin/R

require(DBI)
require(RSQLite)

inpath = '~/p/citu_scraper/data/part0_to_part_5.csv'
outpath = '~/p/citu_scraper/data/work.db'

q <- read.csv(inpath, stringsAsFactors = F, sep='\t')

q$X <- NULL

names(q) <- 'company_name'

q$website_url <- '0'

mydb <- dbConnect(RSQLite::SQLite(), outpath)
dbWriteTable(mydb, 'website', q)

dbDisconnect(mydb)

