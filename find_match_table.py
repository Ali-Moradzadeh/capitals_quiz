from all_server_dbs_handle import Server_Database_Handling as serverDBHand

class FindMatchTable :
	
	__host = "host"
	__user = "user"
	__password = "password"
	__database = "database"
	__dbDetailes = None
	__dbHandObj = None
	__column_names = None
	__dict_k_key_v_columnNames = None
	
	
	def __init__(self, dbDetailes) :
		
		self.__dbDetailes = dbDetailes
		
		self.__dbHandObj = serverDBHand(dbDetailes[self.__host], dbDetailes[self.__user], dbDetailes[self.__password], dbDetailes[self.__database])
		
		if self.__dbHandObj.checkConnection() :
			
			pass
		else :
			print("connection falied")
		
		
	def isTableValid(self, table, columnsFlag) :
		
		if not self.__dbHandObj.tableExist(table) :
			print("table not found.")
			return False

		self.__column_names = self.__dbHandObj.getColumns(table)

		print(f"\ncolumn names are : {self.__column_names}\n")

		if not len(self.__column_names) == len(columnsFlag):

			print(f"table must have exactly {len(columnsFlag)} columns")
			return False

		self.__dict_k_key_v_columnNames = self.__dbHandObj.defineEachColumnStoreWhatData(table, columnsFlag)

		return True
		
		
	def getColumnDict(self) :
		
		return self.__dict_k_key_v_columnNames

		
		
		
		