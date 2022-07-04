class Data_handling :

	__used_column_names = []
	__column_username = "username"
	__column_email = "email"
	__column_password = "password"
	__column_score = "score"

	__columns = [__column_username,__column_email, __column_password, __column_score]

	__columns_index = {__column_username : 0, __column_email : 1, __column_password : 2, __column_score :3}

	def __init__(self, table, allDBsHandleObj) :

		self.__serverDBsHand = allDBsHandleObj
		self.__db = allDBsHandleObj.getDB()
		self.__cursor = self.__db.cursor()
		self.__table = table
		self.__column_names = None
		self.__dict_k_key_v_columnNames = None


	def isTableValid(self) :
		if not self.__serverDBsHand.tableExist(self.__table) :
			print("table not found.")
			return False

		self.__column_names = self.__serverDBsHand.getColumns(self.__table)

		print(f"\ncolumn names are : {self.__column_names}\n")

		if not len(self.__column_names) == 4 :

			print("table must have exactly 4 columns")
			return False

		self.__dict_k_key_v_columnNames = self.__serverDBsHand.defineEachColumnStoreWhatData(self.__table, self.__columns)

		return True


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


