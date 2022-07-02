import re
from data_handling import Data_handling as db


def __invalidEmail(email) :
	
	if email.count("@") == 1 and email[email.index("@"):].count(".") == 1 and not "@." in email and not (email.startswith("@") and email.startswith(".") and email.endswith(".")) :
		return False
		
	else :
		
		print("INVALID EMAIL FORM.")
		return __checkValue("email")

				
def __checkValue(key) :
	
	legal_chrs_dic = {"username" : "[a-zA-Z0-9_.-]", "email" : "[a-zA-Z0-9_@.-]"}	
	value = input(f"{key} : ")
	
	if(key == "password") and len(value) < 8 :
		print("Too Short Password. Try Again.")		
		return __checkValue(key)
		
	if key != "password" and (value == "" or len(re.findall(legal_chrs_dic[key],value)) != len(value)) :	
		print(f"ILLEGAL CHARACTERS. TRY AGAIN WITH THESE CHARACTERS : {legal_chrs_dic[key]}")	
		return __checkValue(key)
				
	if key == "email" :
			__invalidEmail(value)	
			
	return value

	
def __wanaTryAgainInRegister(username,email, password) :
	tryAgain = input("wana Try Again ?? (y/n) : ").lower()
	if tryAgain == "y" :
		
		print("\nRetrying Register : ")
		__sign_up()	
		
	elif tryAgain == "n" :
		
		if db().registerPlr(username, email, password) :
			print("singing up successfully done.")
			
		else : 
			start()
			
	else :
		print("Invalid Input.")
		__wanaTryAgainInRegister(username, email, password)
	
	
def __sign_in() :
	pass


def __sign_up() :
	
	username = __checkValue("username")
	email = __checkValue("email")
	password = __checkValue("password")

	print(f"\nyour informations are :\n\t{username = }\n\t{email = }\n\t{password = }\n")
	
	__wanaTryAgainInRegister(username, email, password)
	
	
def start() :
	
	print("sign up or sign in ??\n")
	sign = input('type "up" for sign up / "in"" for sign_in : ').lower()

	if sign == "up" :
		__sign_up()
		
	elif sign == "in" :
		__sign_in()
		
	else :
	
		print("INVALID INPUT, TRY AGAIN.")
		start()
		
