'''
Created on 13 aug. 2015

@author: Drikus Roor
'''

# Import url library for http requests
import urllib3

# Import BeautifulSoup, a library for data scraping
from bs4 import BeautifulSoup
import json

http = urllib3.PoolManager()

def GetHtml(url):
    r = http.request('GET', url)
    return r.data

# Function that returns a list of movie objects based on a given search term
# A movie objects consists of a dictionary which includes the imdb url, 
# the imdb id, the name of the movie, and the year of the movie
def GetMovieList(search_term):
    movie_list = []
    amount_results = 1 # Declares the maximum amount of search results that will be returned through the movie list
    domain = 'http://www.imdb.com/'
    url_first = 'find?q='
    url_last_optional = '&s=tt&ttype=ft&ref_=fn_ft'
    search_url = domain + url_first + search_term + url_last_optional
    search_url = search_url.replace(' ', '+')
    
    # Requests html of retrieved page
    movie_list_html = GetHtml(search_url)
    
    # Turns this html into a BeautifulSoup object
    movie_list_soup = BeautifulSoup(movie_list_html, 'html.parser')

    # Scrapes the rows of the search results, extracts information about a movie
    # This information will be added to the movie list in a dictionary
    for row in movie_list_soup.table.find_all('tr'):
        
        # Declares dictionary for information about movie
        movie_meta = {}

        # Extracts all row information and stores it into the movie list as a dictionary
        for cell in row.find_all('td', class_='result_text'):
            movie_meta['url'] = cell.a.get('href')
            url = movie_meta['url']
            movie_meta['id'] = url[7: 16]
            movie_meta['name'] = cell.a.string
            cell.a.extract()
            year = cell.contents[1]
            movie_meta['year'] = year[2:6]
            movie_list.append(movie_meta)

    print("Amount of hits for this search term: " + str(len(movie_list)))
    if len(movie_list) >= amount_results: # Only looks for the first 5 or less results
        movie_list = movie_list[0:amount_results]
    return movie_list

# Function that scrapes cast information of a movie through a given imdb id
# Returns a list of dictionaires that include an actor's url, imdb id and name
def GetCastList(movie_id):
    cast_list = {} #to assign roles to persons, a dictionary is used
    
    domain = 'http://www.imdb.com/'
    url_first = 'title/'
    url_middle = movie_id
    url_last = '/fullcredits?ref_=tt_cl_sm#cast'
    search_url = domain + url_first + url_middle + url_last
    print(search_url)
    cast_info_html = GetHtml(search_url)
    cast_info_soup = BeautifulSoup(cast_info_html, 'html.parser')

    cast_list = []

    
    actor_list_soup = cast_info_soup.find("table", class_="cast_list")

    # Extracts information about cast and stores each actor's basic information in cast_list
    try:
        for row in actor_list_soup.find_all("tr"):
            actor = {}
            link = row.find_all("a")
            #only extracts the link urls and texts from rows that actually contain links
            if link != None:
                if len(link) > 0:
                    link = link[1]
                    actor['url'] = link.get('href')
                    actor['id'] = actor['url'][6:15]
                    actor['name'] = link.span.string
                    actor_birth_dict = GetActorInformation(actor['id'])
                    print(actor_birth_dict)
    except:
        actor = "No actors in this movie."
        print(actor)
        cast_list.append(actor)

    return cast_list

# 
def GetActorInformation(actor_id):
    actor_birth_dict = {}
    domain = 'http://www.imdb.com/'
    url_first = 'name/'
    url_middle = actor_id
    url_last = ''

    search_url = domain + url_first + url_middle + url_last
    print(search_url)
    actor_info_html = GetHtml(search_url)
    actor_info_soup = BeautifulSoup(actor_info_html, 'html.parser')
    try:
        actor_birth_soup = actor_info_soup.find_all("div", class_="txt-block")[1]
    except IndexError:
        actor_birth_soup = False
        print("Oops, no information about birth date!")
    if actor_birth_soup:
        #Checks whether there is a birth date, or throws exception
        try:

            actor_birth_date = actor_birth_soup.time.find_all("a")[0:2]
            actor_birth_dict["Birth Date: "] = actor_birth_date[0].string + ", " + actor_birth_date[1].string
        except:
            actor_birth_dict["Birth Date: "] = "Unknown"

        # Checks whether there is a birth place, or throws exception
        try:
            actor_birth_place_link = actor_birth_soup.find_all("a")[2]
            # Checks whether the link above refers to birth place or not
            if "birth_place" in str(actor_birth_place_link):
                print("Birth place is known!")
                actor_birth_place = actor_birth_place_link.string
                actor_birth_dict["Actor Birth Place: "] = actor_birth_place
                actor_type = actor_birth_place[-3:]

                if actor_type != "USA":
                    actor_type = "ROME"
                actor_birth_dict["Rome or US: "] = actor_type
            else:
                actor_birth_dict["Actor Birth Place: "] = "Unknown (no country, but year)"
                actor_birth_dict["Rome or US: "] = "Unknown (no country, but year)"
        except:
            actor_birth_dict["Actor Birth Place: "] = "Unknown"
            actor_birth_dict["Rome or US: "] = "Unknown"
        #print(actor_birth_dict)
    if actor_birth_soup:
        return actor_birth_dict
    else:
        return {"Birth Date: " : "Unknown (soup)", "Actor Birth Place: " : "Unknown (soup)", "Rome or US: ": "Unknown (soup)"}

# Function that scrapes all information about movies and its cast
# through a list of search terms
# Returns a list of movie objects
# These movie objects include a list of cast member dictionaries,
# which contain information about the respective cast member
def GetAllInformation(search_term_list):

    end_results = []

    for search_term in search_term_list:
        search_term_results = {}
        search_results_list = GetMovieList(search_term)
        print(search_results_list)
        search_results_list = search_results_list[0:2] #only the first result

        for search_result in search_results_list:
            search_result_id = search_result['id']
            print(search_result_id)
            cast_list = GetCastList(search_result['id'])
            search_term_results[search_result_id] = cast_list

        end_results.append(search_term_results)

    return end_results