'''
Created on 18 aug. 2015

@author: Drikus
'''
from moviesearchlist import *
import json

def AskQuestion(question_string):
	yes = set(['yes','y', 'ye', 'yeah', ''])
	no = set(['no','n'])
	question_string += ' (Y/n): '
	answer_string = raw_input(question_string).lower()
	if answer_string in yes:
	   answer_boolean = True
	else:
	   answer_boolean = False
	return answer_boolean

def PromptSearchTerms():
	list_of_search_terms = []
	repeat_question = True
	while(repeat_question):
		search_term = raw_input("Enter a search term: ")
		list_of_search_terms.append(search_term)
		# Asks whether the user wants to input another search term
		yes = set(['yes','y', 'ye', 'yeah', ''])
		no = set(['no','n'])
		repeat_question = AskQuestion("Do you want to enter another search term?")

	export_json = AskQuestion("Do you want to export the results to json?")

	return list_of_search_terms

# Create a list of movies of which you want to scrape all metadata from
# sample_list_of_search_terms = ['Sleuth', 'Paranormal Activity']
list_of_search_terms = PromptSearchTerms()
movies_information = GetAllInformation(list_of_search_terms, 1)
print(movies_information)

with open('pickle.txt', 'w') as outfile:
	json.dump(movies_information, outfile)
