import re
from data_handling import Data_handling as db

__db_handling_obj = None

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

	
def __wanaContinueInRegister(username,email, password) :
	
	go_on = input("wana Try Again ?? (y/n) : ").lower()
	
	if go_on == "y" :
		
		if __db_handling_obj.registerPlr(username, email, password) :
			
			print("\nsinging up successfully done.")
			
		start(__db_handling_obj)
		
	elif go_on == "n" :
		
		print("\nRetrying Register : ")
		__sign_up()
		
	else :
		print("Invalid Input.")
		__wanaContinueInRegister(username, email, password)
	
	
def __sign_in() :
	
	sign_in_type = input("sign in with username or email ?? (u/e) : ").lower()
	
	byUser = sign_in_type == "u"
	byEmail = sign_in_type == "e"
	
	if not (byUser or byEmail) :
		
		print("invalid input.")
		__sign_in()
		
	key = "username" if byUser else "email"
	
	value = input(f"{key} : ")
	password = input("password : ")
	
	result = __db_handling_obj.allowedToLoginByEmail(value, password) if byEmail else __db_handling_obj.allowedToLoginByUsername(value, password)
	
	if result :
		print("\nSuccessfully logged in.")
		#continue to take quiz
		
def __sign_up() :
	
	username = __checkValue("username")
	email = __checkValue("email")
	password = __checkValue("password")

	print(f"\nyour informations are :\n\t{username = }\n\t{email = }\n\t{password = }\n")
	
	__wanaContinueInRegister(username, email, password)
	
	
def start(db_handling_obj) :
	
	global __db_handling_obj
	__db_handling_obj =  db_handling_obj
	
	print("sign up or sign in ??\n")
	sign = input('type "up" for sign up / "in"" for sign_in : ').lower()

	if sign == "up" :
		__sign_up()
		
	elif sign == "in" :
		__sign_in()
		
	else :
	
		print("INVALID INPUT, TRY AGAIN.")
		start(db_handling_obj)
		
