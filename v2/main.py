from feedparser import feedparser
from db import Database
import urllib2, os, datetime, time
from HTMLParser import HTMLParser
import htmlentitydefs

""" 
This script aggregates news articles from a collection of rss feeds
"""

rssFeeds =  [
		"http://rss.cnn.com/rss/money_markets.rss",
		"http://feeds.marketwatch.com/marketwatch/stockstowatch?format=xml",
		"http://feeds.reuters.com/news/wealth",
		"http://feeds.reuters.com/reuters/businessNews",
		"http://feeds.reuters.com/reuters/companyNews",
		"http://finance.yahoo.com/news/category-earnings/rss",
		"http://finance.yahoo.com/news/category-ipos/rss",
		"http://finance.yahoo.com/news/category-m-a/rss",
		"http://finance.yahoo.com/news/category-stocks/rss",
		"http://www.cnbc.com/id/100003241/device/rss/rss.html",
		"http://www.cnbc.com/id/15839135/device/rss/rss.xml",
		"http://www.cnbc.com/id/15839069/device/rss/rss.html"
	]

# dev path
#relativePath = os.getcwd() + "/rss_output/"

# production value
relativePath = os.getcwd() + "/labs/quantAlgo/rss_output/"


numInserted = 0
numError = 0
numFound = 0


class HTMLTextExtractor(HTMLParser):
	"""
	Special class for sanitizing HTML input
	"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()

def getPublishTime(article):
	"""
	MySQL date format: YYYY-MM-DD HH:MM:SS
	"""
	pubDate = article['published_parsed'];
	dt = datetime.datetime.fromtimestamp(time.mktime(pubDate))
	path = dt.strftime("%Y-%m-%d %H:%M:%S")
	return path

def buildArticlePath(article):
	pubDate = article['published_parsed'];
	dt = datetime.datetime.fromtimestamp(time.mktime(pubDate))
	path = dt.strftime("%Y/%m/%d/")
	return path

def getArticleSummary(article):
	"""
	Strips out html tags from the summaries, returns plaintext
	"""
	return cleanUpText(html_to_text(article['summary_detail']['value'])).replace("\n",'').strip()

def getArticleSource(article):
	return cleanUpText(article['summary_detail']['base'])

def cleanUpText(text):
	"""
	Function handles encoding of xml file

	Xml usually based in as UTF-8. We want to return 
	Ascii version for python
	"""
	return text.encode('ascii','ignore')

db = Database()
db.connect()
for feed in rssFeeds:
	rss = feedparser.parse(feed) #RSS object

	numFound += len(rss['entries'])
	print("Found a total of "+str(numFound)+" articles from rss feed: "+str(feed))
	for entry in rss['entries']:
		outputDir = relativePath + buildArticlePath(entry)
		
		if not os.path.exists(outputDir):
			os.makedirs(outputDir)
		# Download the article
		link = entry['link']
		originalTitle = cleanUpText(entry['title'])
		
		formattedTitle = originalTitle.replace(' ','_').replace('/','-').replace("'",'')
		
		relFilePath = buildArticlePath(entry) + formattedTitle+".html"
		filePath = outputDir+formattedTitle+".html"

		if not os.path.exists(filePath):	
			print("Downloading: "+link)
			try:
				u = urllib2.urlopen(link)
			except urllib2.HTTPError as e:
				# Handle error if link fails to load (404)
				numError += 1
				print("[ERROR] failed to download url: "+link)
				print(e)
				break
			except urllib2.URLError as e:
				numError += 1

				print("[ERROR] failed to open url: "+link)
				print(e)
				break
			localFile = open(filePath, 'w')
			localFile.write(u.read())
			localFile.close()

			db.insertArticleEntry(originalTitle, getArticleSource(entry),getPublishTime(entry),getArticleSummary(entry),relFilePath)
			numInserted += 1

db.updateLog(numInserted, numError, numFound)
timestamp = datetime.datetime.now().strftime("%x %X")
print("[{0}] JOB DONE! Downloaded {1} articles.").format(timestamp,numInserted)