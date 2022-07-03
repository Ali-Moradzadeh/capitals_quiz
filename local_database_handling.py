class Data_handling :

	__columns_key = {"username" : 0, "email" : 1, "password" : 2, "score" :3}

	__RECORD_SEPERATOR = "\u2661\n"
	__INFOS_SEPPERATOR = "\u2662"
	__DB_NAME = "Database.txt"

	__file_write = open(__DB_NAME, "a+")

	__file_read = open(__DB_NAME,"r")

	def getReadableFile(self) :

		return self.__file_read


	def clear(self) :

		toWrite = open(self.__DB_NAME, "w")
		toWrite.write("")
		toWrite.close()


	def infoExist(self, info, key) :

		result = False
		for record in self.getRecords() :

			if record.split(self.__INFOS_SEPPERATOR)[self.__columns_key[key.lower()]] == str(info) :
				result = True
				break

		return result


	def getRecords(self) :
                self.__file_read.seek(0)
                return self.__file_read.read().split(self.__RECORD_SEPERATOR)[:-1]


	def getRowByRecord(self, value, key) :

		row = tuple(record.split(self.__INFOS_SEPPERATOR) for record in self.getRecords() if record.split(self.__INFOS_SEPPERATOR)[self.__columns_key[key]] == value)
		return row if len(row) == 0 else row[0]


	def recordsCount(self) :

		return len(self.getRecords())


	def registerPlr(self, username, email, password) :

		result = True

		if not (self.infoExist(username, "username") or self.infoExist(email, "email")) :

			self.__file_write.write(f"{username}{self.__INFOS_SEPPERATOR}{email}{self.__INFOS_SEPPERATOR}{password}{self.__INFOS_SEPPERATOR}0{self.__RECORD_SEPERATOR}")
			self.__file_write.close()

		elif self.infoExist(username, "username") :

			print("username already exist try with another")
			result = False

		elif self.infoExist(email, "email") :

			print("email already exist try with another")
			result = False

		return result


	def __allowedToLoginByKey(self, value, key, password) :

		result = False

		if self.infoExist(value, key) :
			savedPassword = self.getRowByRecord(value, key)[self.__columns_key["password"]]

			if password == savedPassword :
				result = True

		if not result :
			print(f"{key} or password is incorrect")

		return result


	def allowedToLoginByEmail(self, email, password) :

		return self.__allowedToLoginByKey(email, "email", password)


	def allowedToLoginByUsername(self, username, password) :

		return self.__allowedToLoginByKey(username, "username", password)

