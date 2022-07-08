import mysql.connector as con
import all_server_dbs_handle as allServerDB
import functools

db = None

host = "127.0.0.1"
user = "alimo"
password = "72943816002123"
database = "capital_quiz_plrs"
table = "capitals"

obj = allServerDB.Server_Database_Handling(host, user, password, database)
db = obj.getDB()


def getRows() :
	
	global db
	global table
	global ast
	
	cursor = db.cursor()
	
	cursor.execute(f"select * from {table}")
	rows = cursor.fetchall()
	return rows
	
	
def __getColumnRecords(columnName) :

	global db
	global table
	global obj
	
	if columnName in obj.getColumns(table) :
		
		cursor = db.cursor()
		cursor.execute(f"select {columnName} from {table}")
	
		return tuple(country[0] for country in cursor.fetchall())
		
	return None


def getCountries() :
	return __getColumnRecords("country")


def getCapitals() :
	return __getColumnRecords("capital")
	

def getHardnesses() :
	return __getColumnRecords("hardness")

	
def getHardnessByKey(value, key) :
	
	return getHardnesses()[list(__getColumnRecords(key)).index(value)]
	
	
def getCountryByCapital(capital) :
	
	return getCountries()[list(getCapitals()).index(capital)]
	
def getCapitalByCountry(country) :
	
	return getCapitals()[list(getCountries()).index(country)]
