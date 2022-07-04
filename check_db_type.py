import confirm_identification as confirmID
import server_database_handling as server_db_handling
import local_database_handling as local_db_handling
import all_server_dbs_handle as allDBsHandle

__host = "host"
__username = "user"
__password = "password"
__database = "database"
__table = "table"
__infos = (__host, __username, __password, __database, __table)
__db_handling_obj = None
__db = None
__detailes = None
__DBsHandle = None

def __getDbInfos() :
	
	global __detailes
	__detailes = {x : input(f"{x} : ") for x in __infos}
	
def whereToSaveDatas() :
	
	haveDb = input("do you have any server side databade to save account informations ?? (y/n) : ").lower()

	if haveDb == "y" :
		__getDbInfos()
		__DBsHandle = allDBsHandle.Server_Database_Handling(__detailes[__host], __detailes[__username],__detailes[__password], __detailes[__database])
		
		if __DBsHandle.checkConnection() :
			print("Successfully Connected.")
			go_on = input("Continue ?? (y for yes anyother for no) : ").lower()
			__db_handling_obj = server_db_handling.Data_handling(__detailes[__table], __DBsHandle)
		
			if go_on == "y" and __db_handling_obj.isTableValid():
				
			
				confirmID.start(__db_handling_obj)
			
			else :
				print("connection falied.")
				whereToSaveDatas()
			
		else :
			
			whereToSaveDatas()
			
	elif haveDb == "n" :
		
		print("players informations have been saved in 'Database.txt' file in project main directory.")
		
		__db_handling_obj = local_db_handling.Data_handling()
		
		confirmID.start(__db_handling_obj)
	else :
		print("invalid input. try again")
		whereToSaveDatas()
		
		
whereToSaveDatas()
