import mysql.connector as connector

class Server_Database_Handling :
	
	def __init__(self, host, user, password, database) :
		
		self.__host = host
		self.__user = user
		self.__password = password
		self.__database = database
		self.__db = None
		self.__cursor = None
	
	def getColumnNamesQuery(self, table) :
		
		return f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.__database}' AND TABLE_NAME = '{table}'"
	
	
	def checkConnection(self) :
		
		try :
			self.__db = connector.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__database)
			
			self.__cursor = self.__db.cursor()
			return True
			 
		except ConnectionError :
			
			return False
	
	def getDB(self) :
		
		if self.checkConnection() :
				return self.__db
				
		return None
				
	def tableExist(self, table) :
		
		if self.checkConnection() :
			
			query = "show tables"
			
			self.__cursor.execute(query)
			tables = self.__cursor.fetchall()
			
			result = False
			for _table in tables :
				if _table[0] == table :
					result = True
					break
				
			return result
			
		return False
		
		
	def columnExistInTable(self,  table, column) :
		
		if self.tableExist(table) :
			
			self.__cursor.execute(self.getColumnNamesQuery(table))
			
			result = False
			for _column in self.__cursor.fetchall() :
				if(_column[0]) == column :
					result = True
					break
				
			return result
			
		return False
		
	def getColumns(self, table) :
		
		if self.tableExist(table) :
			self.__cursor.execute(self.getColumnNamesQuery(table))
			_columns = self.__cursor.fetchall()
			columns = tuple(column[0] for column in _columns)
			
			return columns
			
		return None
		
	
	def getColumnsCount(self, table) :
		
		if self.tableExist(table) :
			
			return len(self.getColumns(table))
			
		return None
	
	
	def getColumnIndex(self, table, column) :
		
		if self.columnExistInTable(table, column) :
			
			self.__cursor.execute(self.getColumnNamesQuery(table))
			columns = self.__cursor.fetchall()
			return tuple(columns.index(_column) for _column in columns if _column[0] == column)[0]
		
		return None
	
	def defineEachColumnStoreWhatData(self, table, dataFlags) :
		
		columns = self.getColumns(table)
		
		dic = None
		if columns != None and len(columns) == len(dataFlags) :
			
			print(f"available flages : \n\t {dataFlags}\n")
			dic = {}
			i = 0
			while len(dic) != len(columns) :
				
				flag = dataFlags[i]
				
				chosenColumn = input(f"which column use for storing '{flag}' : ")
				
				if chosenColumn not in columns :
					print("input column not found.")
					continue
				
				if chosenColumn in dic.values() :
					print("column has previously been chosen. try with another")
					continue
					
				if flag in dic.keys() :
					print(f"{flag} flag has already been used for a column. try another flag.")
					continue
				
				dic[flag] = chosenColumn
				i+=1
				
			return dic