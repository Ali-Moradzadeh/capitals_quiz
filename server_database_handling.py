#import mysql.connector as connector

class Data_handling :
	
	__used_column_names = []
	__column_username = "username"
	__column_email = "email"
	__column_password = "password"
	__column_score = "score"

	__columns = [__column_username,__column_email, __column_password, __column_score]
	
	__columns_index = {__column_username : 0, __column_email : 1, __column_password : 2, __column_score :3}
	
	def __init__(self, detailes, db) :
		
		self.__db = db
		self.__detailes = detailes
		self.__cursor = db.cursor()
		self.__table = detailes["table"]
		self.__database = detailes["database"]
		
	def checkValidTable(self) :
		
		query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{self.__database}' AND TABLE_NAME='{self.__table}'"
		
		self.__cursor.execute(query)
		fet = self.__cursor.fetchall()
		
		self.__column_names = tuple(x[0] for x in fet)
		
		print(f"\ncolumn names are : {self.__column_names}\n")
		
		result = len(self.__column_names) == 4
		if not result :
			
			print("Error. table must have exactly 4 columns")
			return result
		
		columns = {key : {"column_name" : self.__controlTypedColumnName(key), "column_index" : self.__controlTypedColumnIndex() - 1} for key in self.__columns}
			
		self.__column_names = [V["column_name"] for K,V in columns.items()]

		index = lambda key : tuple(self.__columns.index(K) for K,V in columns.items() if V["column_name"] == key)[0]

		self.__column_names.sort(key = index)
		
		
		
		self.__column_username, self.__column_email, self.__column_password, self.__column_score = self.__column_names
			
		return result
		
	def __controlTypedColumnName(self, key) :
		
		typedName = input(f"column name for storing {key} : ")
		
		if typedName in self.__column_names and typedName not in self.__used_column_names :
			
			self.__used_column_names.append(typedName)
			return typedName
			
		elif typedName not in self.__column_names :
			
			print("please type correct column name , which you type is not a column name in table")
	
		else : 
			print("this column has already been used try another one")
		
		self.__controlTypedColumnName(key)
		
		
	def __controlTypedColumnIndex(self) :
		
		indexStr = input("this column's number in table : ")
		
		try :
			
			index = int(indexStr)
			
			if index < 1 or index > 4 :
				
				print("please insert just 1 or 2 or 3 or 4")
				return self.__controlTypedColumnIndex()
		
			else :
				return index
			
		except ValueError :
			
			print("please insert just 1 or 2 or 3 or 4")
			return self.__controlTypedColumnIndex()
	
	
	def registerPlr(self, username, email, password) :
	
		result = True
		
		if not (self.infoExist(username, self.__column_username) or self.infoExist(email, self.__column_email)) :
		
			query = f"insert into {self.__table}({self.__column_username}, {self.__column_email}, {self.__column_password}, {self.__column_score}) values ('{username}', '{email}', '{password}', 0)"
	
			self.__cursor.execute(query)
			self.__db.commit()
		
		elif self.infoExist(username, self.__column_username) :
		
			result = False
			print("username already exist. try with another")
		
		elif self.infoExist(email, self.__column_email) :
		
			result = False
			print("email already exist try with another")
		
		return result
		
	def getRecords(self) :
	
		query = f"select * from {self.__table}"
	
		self.__cursor.execute(query)
		return self.__cursor.fetchall()
	
	
	def recordsCount(self) :
		return len(self.getRecords())
	
	
	def getRowByRecord(self, value, key) :
	
		query = f"select * from {self.__table} where {key} = '{value}'"
	
		self.__cursor.execute(query)
		return self.__cursor.fetchall()[0]
	

	def infoExist(self, value, key) :
	
	#print(__cursor.column_names())
		query = f"select {key} from {self.__table} where exists(select {key} from {self.__table} where {key} = '{value}')"
	
		self.__cursor.execute(query)
		x = self.__cursor.fetchall()
	
		return len(x) != 0
	

	def allowedToLoginByEmail(self, value, password) :
	
		return self.__allowedToLoginByKey(value, self.__column_email, password)


	def allowedToLoginByUsername(self,value, password) :
	
		return self.__allowedToLoginByKey(value, self.__column_username, password)

	
	def __allowedToLoginByKey(self, value, key, password) :
	
		result = self.infoExist(value, key) and self.getRowByRecord(value, key)[2] == password
		if not result :
			
			print(f"{key} or password is incorrent.")
			
		return result
			

