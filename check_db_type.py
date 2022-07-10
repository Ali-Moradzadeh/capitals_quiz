from os import system
import confirm_identification as CONF_ID
import server_database_handling as server_db_handling
import local_database_handling as localDB
from all_server_dbs_handle import Server_Database_Handling as allDBsHandle
from game_detailes import GameDetailes

__host = "host"
__username = "user"
__password = "password"
__database = "database"
__table = "table"
__infos = (__host, __username, __password, __database, __table)
db_handling_obj = None
__db = None
__detailes = {}
__DBsHandle = None
__haveServerDb = None
__isDBServerSide = False

def __getDbInfos() :
	
	global __detailes
	
	i = 0
	while len(__detailes) != len(__infos) :
		
		typed = input(f"{__infos[i]} : ")
		confirm = input("confirm ? (y) : ").lower()
		
		if confirm != "y" :
			continue
		
		__detailes[__infos[i]] = typed
		i += 1
		


def __showGameDetailesOrGoToIdentification() :
	
	opinion = input("\nshow game detailes or continue to player identification ??\n-type 'd' to show game detailes\n-type 'p' to continue player identification : ").lower()
	
	system("clear")
	if opinion == 'd' :
		GameDetailes(db_handling_obj).start()
	
	elif opinion == 'p' :
		CONF_ID.start(db_handling_obj)
		
	else : 
		print("invalid input.")
		return __showGameDetailesOrGoToIdentification()


def whereToSaveDatas() :
	
	global __haveServerDb
	__haveServerDb = input("do you have any server side databade to save account informations ?? (y/n) : ").lower()
	
	
	if __haveServerDb == "y" :
		
		global __isDBServerSide
		__isDBServerSide = True
		
		__getDbInfos()
		global __DBsHandle
		__DBsHandle = allDBsHandle(__detailes[__host], __detailes[__username],__detailes[__password], __detailes[__database])
		
		if __DBsHandle.checkConnection() :
			print("Successfully Connected.")
			go_on = input("Continue ?? (y for yes anyother for no) : ").lower()
			global db_handling_obj
			db_handling_obj = server_db_handling.Data_handling(__detailes[__table], __DBsHandle)
			
			CONF_ID.dbObj = server_db_handling
		
			if go_on == "y" and db_handling_obj.isTableValid():
				
				__showGameDetailesOrGoToIdentification()
			
			else :
				print("connection falied.")
				whereToSaveDatas()
			
		else :
			
			whereToSaveDatas()
			
	elif __haveServerDb == "n" :
		
		print("players informations have been saved in 'Database.txt' file in project main directory.")
		
		db_handling_obj = localDB.Data_handling()
		
		__showGameDetailesOrGoToIdentification()
		
		
	else :
		print("invalid input. try again")
		whereToSaveDatas()
		
def getDBDetailesName() :
	
	return __detailes


def isDBServerSide() :
	
	global __isDBServerSide
	return __isDBServerSide
