class Data_handling :
	
	__columns_key = {"username" : 0, "email" : 1, "password" : 2, "score" :3}
	
	__RECORD_SEPERATOR = "\u2661\n"
	__INFOS_SEPPERATOR = "\u2662"
	info_sep = __INFOS_SEPPERATOR
	
	rec_sep = __RECORD_SEPERATOR
	__DB_NAME = "Database.txt"
	db_name = __DB_NAME
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
		
	def getRecordsList(self) : 
		self.__file_read.seek(0)
		
		return [record.split(self.__INFOS_SEPPERATOR) for record in self.__file_read.read().split(self.__RECORD_SEPERATOR)[:-1]]
		
		
		
	def getRecords(self) :
		self.__file_read.seek(0)
		return self.__file_read.read().split(self.__RECORD_SEPERATOR)[:-1]
		
	def getRowByRecord(self, value, key) :
		
		row = tuple(record.split(self.__INFOS_SEPPERATOR) for record in self.getRecords() if record.split(self.__INFOS_SEPPERATOR)[self.__columns_key[key]] == value)
		
		return row[0] if len(row) != 0 else row
		
		
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
			
			print(savedPassword)
			if password == savedPassword :
				
				result = True
			
			
		if not result :
				print(f"{key} or password is incorrect")
				
		return result
	
	def allowedToLoginByEmail(self, email, password) :
		
		return self.__allowedToLoginByKey(email, "email", password)
				
	def allowedToLoginByUsername(self, username, password) :
		
		return self.__allowedToLoginByKey(username, "username", password)
		
		
	
	def increaseScoreBy(self, username, increased) :
		
		row =self.getRowByRecord(username, "username")
		newScore = int(row[self.__columns_key["score"]]) + increased
		
		records = self.getRecords()
		
		for record in records :
			
			wantedRecord = record.split(self.__INFOS_SEPPERATOR)
			
			if wantedRecord[0] == username :
				index = records.index(record)
				
				wantedRecord[3] = newScore
				
				recordStr = ""
				
				for x in wantedRecord : 
					recordStr += str(x)
					
					if wantedRecord.index(x) != len(wantedRecord) - 1 :
						recordStr += self.__INFOS_SEPPERATOR
					
				
				records[index] = recordStr
				break
				
		
		string = self.__makeDbOfRecordsList(records)
		
		wr = open(self.__DB_NAME, "w")
		wr.write(string)
		wr.close()
					
			
	def __makeRecordOfInfosList(self, listContainInfos) :
		
			record = ""
			for info in listContainInfos :
				
				record += str(info)
				
				if listContainInfos.index(info) != len(listContainInfos) - 1 :
					record += self.__INFOS_SEPPERATOR
					
				else :
					record += self.__RECORD_SEPERATOR
					
			return record
			

	def __makeDbOfRecordsList(self, listContainRecords) :
					
					
			db = ""
			for record in listContainRecords :
				
				recordList = record.split(self.__INFOS_SEPPERATOR)
				
				db += self.__makeRecordOfInfosList(recordList)
			return db


	def executeQuery(self, select, where, orderBy, limit) : 
		
		#compile where condition here
		alldatas = [record for record in self.getRecordsList() if int(record[3]) <= where[1] and int(record[3]) >= where[0]]
		
		#compile orderBy here
		if len(orderBy) != 0 :
			
			index = self.__columns_key[list(orderBy.keys())[0]]
		
			sorting = lambda x : int(x[index]) if index == 3 else x[index]
			alldatasCopy = sorted(alldatas, key = sorting)
			
			if list(orderBy.values())[0] == "desc" :
				alldatasCopy.reverse()
			
			alldatas = list(alldatasCopy)
			del alldatasCopy
		
		p = {list(self.__columns_key.keys())[i] : [record[i] for record in alldatas] for i in range(0,len(self.__columns_key)) if i != 2}
	
		#compile select command here
		result = {choose : p[choose] for choose in select}
		
		#compile limit command here :
		listValues = list(result.values())
		
		y = [[rex[i] for rex in listValues] for i in range(0, len(listValues[0]))]
	
		return y[limit[0] - 1: limit[1]]
		
		
