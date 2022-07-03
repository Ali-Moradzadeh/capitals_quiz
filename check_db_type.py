import os
import mysql.connector as connector
import confirm_identification as txtDb
import server_db_handle
import data_handling

__host = "host"
__username = "user"
__password = "password"
__database = "database"
__table = "table"
__infos = (__host, __username, __password, __database, __table)
__db_handling_obj = None
__db = None
__detailes = None

def __getDbInfos() :
	
	global __detailes
	__detailes = {x : input(f"{x} : ") for x in __infos}
	
def checkConnection() :
	
	__getDbInfos()
	
	try :
		
		global __db
		__db = connector.connect(host = __detailes[__host], user = __detailes[__username], password =  __detailes[__password], database =  __detailes[__database])
		
		print("\nconnect successfully.\n")
		return True
		
	except :
		
		print("\ndatabase connection failed\n")
		return False

def whereToSaveDatas() :
	
	haveDb = input("do you have any server side databade to save account informations ?? (y/n) : ").lower()

	if haveDb == "y" :
		
		if checkConnection() :
			
			go_on = input("Continue ?? (y for yes anyother for no) : ").lower()
			__db_handling_obj = server_db_handle.Data_handling(__detailes, __db)
		
			if go_on == "y" and __db_handling_obj.checkValidTable():
				
			
				txtDb.start(__db_handling_obj)
			
			else :
				
				whereToSaveDatas()
			
		else :
			
			whereToSaveDatas()
			
	elif haveDb == "n" :
		
		print("players informations have been saved in 'Database.txt' file in project main directory.")
		
		__db_handling_obj = data_handling.Data_handling()
		
		txtDb.start(__db_handling_obj)
	else :
		print("invalid input. try again")
		whereToSaveDatas()
		
		
whereToSaveDatas()