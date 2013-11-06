from feedparser import feedparser
import urllib2, os, datetime

""" 
This script aggregates news articles from a collection of rss feeds
"""

today = datetime.date.today();
rssFeeds =  [
		"http://rss.cnn.com/rss/money_markets.rss",
		"http://feeds.marketwatch.com/marketwatch/stockstowatch?format=xml"
	]
todayDir = today.strftime("%Y/%m/%d/")
outputDir = "rss_output/"+todayDir
counter = 0
for feed in rssFeeds:
	rss = feedparser.parse(feed) #RSS object

	#print("\nFound a total of "+str(len(rss['entries']))+" articles from rss feed: "+str(feed))
	for entry in rss['entries']:
		if not os.path.exists(outputDir):
			os.makedirs(outputDir)
		# Download the article
		link = entry['link']
		
		formattedTitle = entry['title'].replace(' ','_').encode('utf8')
		filePath = outputDir+formattedTitle+".html"
		if not os.path.exists(filePath):	
			#print("Downloading: "+link)
			u = urllib2.urlopen(link)
			localFile = open(filePath, 'w')
			localFile.write(u.read())
			localFile.close()
			counter += 1

timestamp = datetime.datetime.now().strftime("%x %X")
print("[{0}] Successfully downloaded {1} articles").format(timestamp,counter)