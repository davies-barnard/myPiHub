import sqlite3 as lite
import os.path


class Database():
	
	#Main Variables
	dbFile = "greenhouse.sdb"
	tables = {
		'archive':
			"""CREATE TABLE IF NOT EXISTS archive (
				ts INT NOT NULL,
				temp REAL
			)""",
	}

	#Operational Variables
	con = None
	
	#Intialisation Method
	def __init__(self):
		
		self.firstTimeRun()
		
		response = self.runQuery("SELECT SQLITE_VERSION()",fetchall=False)
		print (response)
		
		response = self.runQuery("SELECT name FROM sqlite_master WHERE type='table';",fetchall=True)
		print (response)


	def runQuery(self,sql,fetchall):
		data = False
		try:
			if not self.con:
				self.con	 = lite.connect(self.dbFile)
			cur = self.con.cursor()
			cur.execute(sql)
			
			if fetchall:
				data = cur.fetchall()
			else:
				data = cur.fetchone()

		except lite.Error as e:
			print ("Error %s:" % e.args[0])
			sys.exit(1)

		finally:
			if self.con:
				self.con.close()
				self.con = None
				
		return data

#					cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
#					print(cur.fetchall())

#					cur.execute('select * from dances')
#					data=cur.fetchone()
#					print(cur.description)


	"""firstTimeRun Method - If the database does not exist we will create our tables"""
	def firstTimeRun(self):
		
		print ("First Time Run")
		try:		
			self.con = lite.connect(self.dbFile)
			cur = self.con.cursor()
			for tName, tQuery in self.tables.iteritems():
				cur.execute(tQuery)
				print ("Table",tName,"Created")
		except lite.Error as e:
			print ("Error %s:" % e.args[0])
			sys.exit(1)

		finally:
			if self.con:
				self.con.close()
				self.con = None


	"""Add an entry to the archive table"""
	def createArchive(self,tS,tC):		
		try:
			if not self.con:
				self.con	 = lite.connect(self.dbFile)
			cur = self.con.cursor()
			sql = "INSERT INTO archive (ts, temp) VALUES (" + str(tS) + "," + str(tC) + ")"
			res = cur.execute(sql)
			self.con.commit()			
			print (sql)	
		except lite.Error as e:
			print ("Error %s:" % e.args[0])
			sys.exit(1)
		finally:
			if self.con:
				self.con.close()
				self.con = None
			
if __name__ == "__main__": 
	
	from random import uniform
	import time
	
	db = Database()

	response = db.runQuery("SELECT * FROM 'archive'",fetchall=True)
	print (response)

	
#	for i in range (0,10):
#		db.createArchive(time.time(),uniform(-10.0,30.0))
#		time.sleep(0.5)
