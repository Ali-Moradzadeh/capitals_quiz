import all_server_dbs_handle as allServerDB
import check_db_type as whichDB
from find_match_table import FindMatchTable


class question_data_handling :
	
	db = None
	host = None
	user = None
	password = None
	database = None
	table =  None
	
	obj = None
	__columnsFlag = ("country", "capital", "hardness")
	__columns_dict = None


	def __init__(self) :
		
		self.host = whichDB.getDBDetailesName()["host"]
		self.user = whichDB.getDBDetailesName()["user"]
		self.password = whichDB.getDBDetailesName()["password"]
		self.database = whichDB.getDBDetailesName()["database"]
		self.obj = allServerDB.Server_Database_Handling(self.host, self.user, self.password, self.database)
		self.db = self.obj.getDB()
		self.__findMatchTableObj = FindMatchTable(whichDB.getDBDetailesName())
		self.table = self.__getTableName()

		if self.__findMatchTableObj.isTableValid(self.table, self.__columnsFlag) :
			self.__columns_dict = self.__findMatchTableObj.getColumnDict()
			
			
	def everyThingIsOk(self) :
		
		return self.__columns_dict != None
	

	def __getTableName(self) :
		
		string = input("\nyour questions table name : ")
		
		if not self.obj.tableExist(string) :
			print("table not found. try again")
			return self.__getTableName()
			
		return string
		
		
	def getRows(self) :
		
		rows = None
		if self.obj.checkConnection() :
			
			cursor = self.db.cursor()
			cursor.execute(f"select * from {self.table}")
			rows = cursor.fetchall()
		
		return rows
	
	
	def __getColumnRecords(self, columnName) :

		if columnName in self.obj.getColumns(self.table) :
		
			cursor = self.db.cursor()
			cursor.execute(f"select {columnName} from {self.table}")
	
			return tuple(record[0] for record in cursor.fetchall())
		
		return None


	def getCountries(self) :
		return self.__getColumnRecords(self.__columns_dict["country"])


	def getCapitals(self) :
		return self.__getColumnRecords(self.__columns_dict["capital"])
	

	def getHardnesses(self) :
		return self.__getColumnRecords(self.__columns_dict["hardness"])

	
	def getHardnessByKey(self, value, key) :
	
		return self.getHardnesses()[list(self.__getColumnRecords(key)).index(value)]
	
	
	def getCountryByCapital(self, capital) :
	
		return self.getCountries()[list(self.getCapitals()).index(capital)]
	
	
	def getCapitalByCountry(self, country) :
	
		return self.getCapitals()[list(self.getCountries()).index(country)]
