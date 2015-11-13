'''
Created on 18 aug. 2015

@author: Drikus
'''
from moviesearchlist import *

# Create a list of movies of which you want to scrape all metadata from
sample_list_of_movies = ['The Lion King', 'Lord of the Rings']

movies_information = GetAllInformation(sample_list_of_movies, 5)