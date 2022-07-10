from local_database_handling import  Data_handling as localDB

class question_data_handling :
	
	db = None
	__columnsName = ("country", "capital", "hardness")
	
	__file = open(".Datas.enc", "r")
	
	def __init__(self) :
		pass
	
	def everyThingIsOk(self) :
		
		return True
	
	
	def getRows(self) :
		
		result = [record.split(localDB.info_sep) for record in self.__file.read().split(localDB.rec_sep)][:-1]
		
		#print(result)
		return result
	
	
	def __getColumnRecords(self, columnName) :
			
			result = None
			self.__file.seek(0)
			if columnName in self.__columnsName :
				result = [x[self.__columnsName.index(columnName)] for x in self.getRows()]
			self.__file.seek(0)
			return result


	def getCountries(self) :
		return self.__getColumnRecords("country")


	def getCapitals(self) :
		return self.__getColumnRecords("capital")
	

	def getHardnesses(self) :
		return self.__getColumnRecords("hardness")

	
	def getHardnessByKey(self, value, key) :
	
		return int(self.getHardnesses()[list(self.__getColumnRecords(key)).index(value)])
	
	
	def getCountryByCapital(self, capital) :
		
		return self.getCountries()[list(self.getCapitals()).index(capital)]
	
	def getCapitalByCountry(self, country) :
	
		return self.getCapitals()[list(self.getCountries()).index(country)]


obj = question_data_handling()

#print(obj.getCapitals()[0])
