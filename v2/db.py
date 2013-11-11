import MySQLdb, datetime

""" 
Connect to the database to store info about articles
"""

class Database:

	def __init__(self):
		self.host = "db501482795.db.1and1.com"
		self.user = "dbo501482795"
		self.passwd = "mtolive5"
		self.database = "db501482795"

	def connect(self):
		# TODO: surround with try/catch?
		self.db = MySQLdb.connect(self.host, self.user, self.passwd, self.database)
	

	def insertArticleEntry(self,title, src, date, summary, path):

		# you must create a Cursor object. It will let
		#  you execute all the query you need
		cur = self.db.cursor() 

		# Use all the SQL you like
		title = MySQLdb.escape_string(title)
		summary = MySQLdb.escape_string(summary).replace('\n',,'').strip()
		query = "INSERT INTO articles (title,source,publish_date,summary,path) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(title,src,date,summary,path)
		print(query)
		cur.execute(query)


	def updateLog(self, numInserted, numError, numFound):
		cur = self.db.cursor()

		timestamp = datetime.datetime.now().strftime("%Y-%m-%d %X")
		query = "INSERT INTO logs (date, num_inserted, num_error, num_found) VALUES ('{0}','{1}','{2}','{3}')".format(timestamp, numInserted, numError, numFound)
		print(query)
		cur.execute(query)