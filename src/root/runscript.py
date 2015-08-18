'''
Created on 18 aug. 2015

@author: Drikus
'''
from moviesearchlist import *

titanic_list = GetMovieList("daddy")
titanic_url = titanic_list[0:5]

for movie in titanic_list:
    print(movie)

for film in titanic_url:
    print(film['id'])
    soup = GetCastList(film['id'])

example_id = "nm0567162"

example_actor = GetActorInformation(example_id)