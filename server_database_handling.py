from find_match_table import FindMatchTable
import check_db_type as whichDB

obj = None

class Data_handling :

	__used_column_names = []
	__column_username = "username"
	__column_email = "email"
	__column_password = "password"
	__column_score = "score"

	__columns = [__column_username,__column_email, __column_password, __column_score]

	__columns_index = {__column_username : 0, __column_email : 1, __column_password : 2, __column_score :3}
	
	__findMatchTableObj = None
	
	def __init__(self, table, allDBsHandleObj) :
		
		global obj
		obj = self
		
		self.__serverDBsHand = allDBsHandleObj
		self.__db = allDBsHandleObj.getDB()
		self.__cursor = self.__db.cursor()
		self.__table = table
		self.__column_names = None
		self.__dict_k_key_v_columnNames = None
		
		self.__findMatchTableObj = FindMatchTable(whichDB.getDBDetailesName())
		
		
	def isTableValid(self) :
		
		result = self.__findMatchTableObj.isTableValid(self.__table, self.__columns)
		
		self.__dict_k_key_v_columnNames = self.__findMatchTableObj.getColumnDict()
		
		return result
			
		


	def registerPlr(self, username, email, password) :
		result = True
		if not (self.infoExist(username, self.__dict_k_key_v_columnNames[self.__column_username]) or self.infoExist(email, self.__dict_k_key_v_columnNames[self.__column_email])) :

			query = f"insert into {self.__table}({self.__dict_k_key_v_columnNames[self.__column_username]}, {self.__dict_k_key_v_columnNames[self.__column_email]}, {self.__dict_k_key_v_columnNames[self.__column_password]}, {self.__dict_k_key_v_columnNames[self.__column_score]}) values ('{username}', '{email}', '{password}', 0)"
			self.__cursor.execute(query)
			self.__db.commit()

		elif self.infoExist(username, self.__dict_k_key_v_columnNames[self.__column_username]) :
			result = False
			print("username already exist. try with another")

		elif self.infoExist(email, self.__dict_k_key_v_columnNames[self.__column_email]) :

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
		query = f"select * from {self.__table} where {self.__dict_k_key_v_columnNames[key]} = '{value}'"
		self.__cursor.execute(query)
		return self.__cursor.fetchall()[0]


	def infoExist(self, value, key) :
		query = f"select {self.__dict_k_key_v_columnNames[key]} from {self.__table} where exists(select {self.__dict_k_key_v_columnNames[key]} from {self.__table} where {self.__dict_k_key_v_columnNames[key]} = '{value}')"
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



	def __setScore(self) :
		pass



	def increaseScoreBy(self, usename, increased) :
	
		row = self.getRowByRecord(usename, self.__dict_k_key_v_columnNames["username"])
	
		newScore = int(row[3]) + increased
	
		self.__cursor.execute(f"update {self.__table} set {self.__dict_k_key_v_columnNames[self.__column_score]} = {newScore} where {self.__dict_k_key_v_columnNames[self.__column_username]} = '{row[0]}'")
	
		self.__db.commit()
		
		
	def executeQuery(self, select, where, orderBy, limit) :
		
		self.__cursor.execute(f"select {select} from {self.__table} where {where} order by {orderBy} limit {limit}")
		
		return self.__cursor.fetchall()
		
