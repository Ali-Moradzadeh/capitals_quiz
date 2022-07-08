from os import system
import server_database_handling as serverDB
import local_database_handling as localDB


class GameDetailes :

	__column_flag_username = "username"
	__column_flag_email = "email"
	__column_flag_score = "score"
	__column_flags = (__column_flag_username, __column_flag_email, __column_flag_score)
	__columnsDict = {x[0].lower() : x for x in __column_flags}
	__howToOrder = {"a" : "asc", "d" : "desc"}


	def __init__(self, dbObj) :

		self.__dbObj = dbObj
		print(type(dbObj))
		self.__selectedColumns = None
		self.__orderBy = None
		self.__minScore = None
		self.__maxScore = None
		self.__firstRecordFrom = None
		self.__lastRecordIn = None
		self.__mainQuery = ""
		self.__filteredTable = None


	def __numberInputHandle(self, inputMessage) :

		try :
			num= int(input(inputMessage))
			return num

		except ValueError :
			return self.__numberInputHandle(inputMessage)


	def __inputMustBeIn(self, message, defaults) :

		typed = input(message).lower()
		if typed in defaults :
			return typed

		else :
			print(f"invalid input. just type one of these options {list(defaults)}")
			return self.__inputMustBeIn(message, defaults)


	def start(self) :
		self.__getSelectClause()
		self.__getWhereClause()
		self.__getOrderClause()
		self.__getLimitClause()

		select = f"{self.__iterableToStr(self.__selectedColumns)}"
		where = f"{self.__column_flag_score} between {self.__minScore} and {self.__maxScore}"
		orderBy = f"{self.__dictionaryToStr(self.__orderBy, ' ', ', ')}"
		limit = f"{self.__firstRecordFrom - 1},{self.__lastRecordIn - self.__firstRecordFrom + 1}"

		if isinstance(self.__dbObj, serverDB.Data_handling) :

			self.__getDbDetailes(select, where, orderBy, limit)

		elif isinstance(self.__dbObj, localDB.Data_handling) :
			
			self.__getDbDetailes(self.__selectedColumns, [self.__minScore, self.__maxScore], self.__orderBy, [self.__firstRecordFrom, self.__lastRecordIn])
			
		self.__printTable()
		
		
	
	def __getDbDetailes(self, select, where, orderBy, limit) :
		
		self.__filteredTable = self.__dbObj.executeQuery(select, where, orderBy, limit)
		
	
	
	
	def __getSelectClause(self) :
		#system("clear")
		print(f"\nwhich columns you want to show ? just type first letter of one of these choices or type 'stop' to finish :\n {self.__column_flags} : ")
		
		stop = False
		selected = []
		select = None
		
		while not stop :
			
			choose = self.__inputMustBeIn("your choice : ", list(self.__columnsDict.keys()) + ["stop"])
			
			if choose == "stop" :
				stop = True
				continue

			select = self.__columnsDict[choose]

			if select in selected :
				selected.remove(select)
				print(f"{select} removed")

			else :
				selected.append(select)
				print(f"{select} added")

		else :
			if not len(selected) :
				print("select atleast one column")
				return self.__getSelectClause()
			else :
				print(f"selected columns are : {selected}")
				self.__selectedColumns = selected


	def __getWhereClause(self) :

		self.__minScore = self.__numberInputHandle("\nminimum score to show : ")
		self.__maxScore = self.__numberInputHandle("\nmaximum score to show : ")

		if self.__maxScore <= self.__minScore :
			print("max score must greater than min score. try Again")
			self.__getWhereClause()



	def __getOrderClause(self) :
		
		print(f"\nif you want to sort showing detailes by a column just type first letter of its name (skip means no sort):\n columns = {self.__column_flags} : ")
		stop = False
		selected = dict()
		select = None
		
		while not stop :
			
			choose = self.__inputMustBeIn("your  choice : ", list(self.__columnsDict.keys()) + [""])
			
			if choose == "" :
				stop = True
				continue
				
			select = self.__columnsDict[choose]
			
			if select in selected :
				print(f"{select} removed")
				selected.pop(select)
				
			else :
					howToOrder = self.__inputMustBeIn("ascending or descending order ? (a/d) : ", self.__howToOrder.keys())
					
					selected[select] = self.__howToOrder[howToOrder]
					
					print(f"{select} added")
				
		else :
			self.__orderBy = selected
			print(selected)
	
	
	def __getLimitClause(self) :
		
		self.__firstRecordFrom = self.__numberInputHandle("start show detailes from record number ?? : ")
		
		if self.__firstRecordFrom < 1 :
			print("minimum is 1.try again")
			self.__getLimitClause()
			
		else :
			self.__lastRecordIn = self.__numberInputHandle("end show detailes in number ?? : ")
		
			if self.__lastRecordIn < 2 :
				print("minimum is 2.try again")
				self.__getLimitClause()
			else :
				
				if self.__firstRecordFrom >= self.__lastRecordIn :
					print("last record number must greater than first record number.")
					self.__getLimitClause()
		
		
		
	def __iterableToStr(self, iterable) :
		
		result = ""
		for iterated in iterable :
			result += iterated + ", "
		return result[:-2]
			
			
	def __dictionaryToStr(self, dictionary, betweenKeyValueSymbol, betweenItemsSymbol) :
		
		result = ""
		for k, v in dictionary.items() :
			result += f"{k}{betweenKeyValueSymbol}{v}{betweenItemsSymbol}"
		return result[:-len(betweenItemsSymbol)]
		
		
	def __printTable(self) :
		
		sort = [[x[i] for x in self.__filteredTable] for i in range(0, len(self.__filteredTable[0]))]
		
		line = f"{(len(self.__selectedColumns) * 17 + 8) * '-'}\n"
		string = line + "|{:^6}"
		for key in self.__selectedColumns :
			string += "|{:^16}"
		string += "|"
			
			
		print(string.format("num." ,*self.__selectedColumns))
		
		for record in self.__filteredTable :
				
			print(string.format(self.__filteredTable.index(record) + 1, *record))

		print(line)


