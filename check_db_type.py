import confirm_identification as txtDb
import mysql.connector as connector

__host = "host"
__username = "user"
__password = "password"
__database = "database"
__table = "table"

__infos = (__host, __username, __password, __database, __table)

def __getDbInfos() :
	
	return {x : input(f"{x} : ") for x in __infos}
	

def checkConnection() :
	
	infos = __getDbInfos()
	
	try :
		
		connector.connect(host = infos[__host], user = infos[__username], password =  infos[__password], database =  infos[__database])
		
		return True
		
	except ConnectionError :
		
		print("connection failed")
		return False

def whereToSaveDatas() :
	
	haveDb = input("do you have any server side databade to save account informations ?? (y/n) : ").lower()

	if haveDb == "y" :
		
		if checkConnection() :
			
			pass
			
			
	elif haveDb == "n" :
		
		print("players informations have been saved in 'Database.txt' file in project main directory.")
		txtDb.start()
		
	else :
		print("invalid input. try again")
		whereToSaveDatas()
		
		
whereToSaveDatas()