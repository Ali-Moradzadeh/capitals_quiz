from os import  system
from random import  shuffle
from random import randint
import confirm_identification as conf_ID
import local_database_handling as localDB
from question_server_db_handling import question_data_handling as serverQuestDB
from question_local_db_handling import question_data_handling as localQuestDB
import check_db_type as whichDB


def numInputHandler(message) :
	
	number = None
	while number == None :
		
		try : 
			number = int(input(message))
			return number
		
		except ValueError :
			print("invalid input.")
			
	return number
		
		
class quizMaker :
	
	def __init__(self, username) :
		
		self.__username = username
		self.__gameDetailes = conf_ID.dbObj
		
		self.__remainCountries = None
		self.__remainCapitals = None
		self.__correctAnswer = None
		self.__questKey = None
		self.__capitalQuest = False
		self.__countryQuest = False
		self.__userAnswer = None
		self.__questKeyFlag = None
		
		self.__questDbObj = localQuestDB()
		
		if whichDB.isDBServerSide() :
			
			self.__questDbObj = serverQuestDB()
			
		if self.__questDbObj.everyThingIsOk() :
			
			self.__capitals = self.__questDbObj.getCapitals()
			self.__countries = self.__questDbObj.getCountries()
			self.__hardnesses = self.__questDbObj.getHardnesses()
		
		print(f"\nWelCome {self.__username}")

	def __updateScore(self, score) :
		
		conf_ID.dbObj.increaseScoreBy(self.__username, score)
		
		self.start()
		
	def __printQuestion(self) :
		
		rand = randint(0,1)
		self.__countryQuest = rand == 1
		self.__capitalQuest = rand == 0
		
		self.__questKeyFlag = "country" if self.__countryQuest else "capital"

		questionStruct = lambda key : f"which is {key} capital : " if self.__countryQuest else f"city '{key}' is capital of : "
		
		key = None
		if self.__countryQuest :
			
			key = self.__remainCountries.pop(randint(0, len(self.__remainCountries) - 1))
			self.__correctAnswer = self.__capitals[self.__countries.index(key)] 
			
			self.__remainCapitals.remove(self.__correctAnswer)
			
			
		elif self.__capitalQuest :
			key = self.__remainCapitals.pop(randint(0, len(self.__remainCapitals) - 1))
			
			self.__correctAnswer = self.__countries[self.__capitals.index(key)] 
			
			self.__remainCountries.remove(self.__correctAnswer)
			
		self.__questKey = key
		
		print(questionStruct(key))
		
		otherAnswers = self.__getRandomTupleOf(self.__capitals if self.__countryQuest else self.__countries, 3)
		
		answers = list(otherAnswers)
		answers.append(self.__correctAnswer)
		shuffle(answers)
		
		for x in answers :
			print(f"\n\t{answers.index(x) + 1}) {x}")
		
		
		userAnswerChoice = int(self.__getUserAnswer())
		
		self.__userAnswer = answers[userAnswerChoice - 1]
		
		if self.__userAnswer == self.__correctAnswer :
			
			print("correct")
			
		else :
			print("incorrect")
			
		return key
	
	def __getUserAnswer(self) :
		
		typedAns = numInputHandler("correct answer in your opinion ? : ")
		
		if typedAns > 0 and typedAns < 5 :
			return typedAns
			
		else :
			print("type the answer number.")
			return self.__getUserAnswer()
		
		
	def __makeQuestions(self, numbers) :
		
		system("clear")
		system("clear")
		self.__remainCountries = list(self.__countries)
		self.__remainCapitals = list(self.__capitals)
		
		answerdQuestions = 0
		totalGameScore = 0
		tillLastTruthAnswerScore = 0
		correctAnswersCombo = 0
		correctAnswersCount = 0
		wrongAnswerCount = 0
		
		while answerdQuestions <  numbers :
			
			answerdQuestions += 1
			self.__printQuestion()
			
			if self.__userAnswer == self.__correctAnswer :
				
				correctAnswersCount += 1
				correctAnswersCombo += 1
				tillLastTruthAnswerScore += self.__questDbObj.getHardnessByKey(self.__questKey, "country" if self.__countryQuest else "capital")
				
			else :
				wrongAnswerCount += 1
				
				totalGameScore += tillLastTruthAnswerScore * correctAnswersCombo
				
				correctAnswersCombo = 0
				tillLastTruthAnswerScore = 0
				continue
				
			if answerdQuestions == numbers and self.__userAnswer == self.__correctAnswer :
			
				totalGameScore += tillLastTruthAnswerScore * correctAnswersCombo
			
		else :
			print(f"{correctAnswersCount = }\n{wrongAnswerCount = }\nearned scores = {totalGameScore}")
			
			self.__updateScore(totalGameScore)
			
		
	def __getRandomTupleOf(self,tupl, count) :
	
		result = []
		
		while len(result) != count :
			
			result.append(tupl[randint(0, len(tupl) - 1)])
		
		return result
		
	
	def start(self) :
		
		print(f"\nYour Score is now :  {self.__gameDetailes.getRowByRecord(self.__username,'username')[3]}")
		
		wanaQuiz = input("Wana get quiz ?? (y/n) : ").lower()
		
		if wanaQuiz == "y" :
			
			self.__makeQuestions(numInputHandler("type number of questions to answer : "))
			
			
			
		elif wanaQuiz == "n" :
			print(f"goodbye {self.__username}")
			conf_ID.start(conf_ID.dbObj)
		
		else :
			print("invalid input.")
			return self.start()
			
