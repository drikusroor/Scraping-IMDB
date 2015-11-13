'''
Created on 13 aug. 2015

@author: Drikus Roor
'''

# Imports url library for http requests
import urllib3

# Imports BeautifulSoup, a library for data scraping
from bs4 import BeautifulSoup
import json

http = urllib3.PoolManager()
domain = 'http://www.imdb.com/'
amount_results = 2

def GetHtml(url):
    r = http.request('GET', url)
    return r.data

def GetSoup(url):
    print("Url is: " + url)
    html_data = GetHtml(url)
    soup_data = BeautifulSoup(html_data, 'html.parser')
    return soup_data

# Function that returns a list of movie objects based on a given search term
# A movie objects consists of a dictionary which includes the imdb url, 
# the imdb id, the name of the movie, and the year of the movie
def GetMovieList(search_term, amount_results):
    movie_list = []
    search_url = domain + 'find?q=' + search_term + '&s=tt&ttype=ft&ref_=fn_ft'
    search_url = search_url.replace(' ', '+') # Replace spaces with plus characters to use in url
    movie_list_soup = GetSoup(search_url)

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

    if len(movie_list) >= amount_results: # Only looks for the first 5 or less results
        movie_list = movie_list[0:amount_results]
    return movie_list

# Function that scrapes cast information of a movie through a given ImDB id
# Returns a list of dictionaries that include an actor's url, imdb id and name
def GetCastList(movie_id):
    cast_list = []
    search_url = domain + 'title/' + movie_id + '/fullcredits?ref_=tt_cl_sm#cast'
    cast_info_soup = GetSoup(search_url)
    actor_list_soup = cast_info_soup.find("table", class_="cast_list")

    # Extracts information about cast and stores each actor's basic information in cast_list
    try:
        for row in actor_list_soup.find_all("tr"):
            actor = {}
            link = row.find_all("a")

            # Only extracts the link urls and texts from rows that actually contain links
            if link != None:
                if len(link) > 0:
                    link = link[1]
                    actor['url'] = link.get('href')
                    actor['id'] = actor['url'][6:15]
                    actor['name'] = link.span.string
                    print("==========")
                    print(actor['name'])
                    actor_birth_dict = GetActorInformation(actor['id'])
    except:
        actor = "No actors in this movie."
        cast_list.append(actor)

    return cast_list

# Function that scrapes birth date and place information from the IMDb page of the actor
# Takes an ImDB actor id as parameter (e.g. nm0000100 for Rowan Atkinson)
# Returns a dictionary with information about the birth date and place
# E.g. {"Actor Birth Date: " : "November 10, 1980", "Actor Birth Place: ": "Los Angeles, California, USA"}
def GetActorInformation(actor_id):
    actor_birth_dict = {}
    search_url = domain + 'name/' + actor_id + ''
    actor_info_soup = GetSoup(search_url)

    try:
        actor_birth_soup = actor_info_soup.find_all("div", class_="txt-block")[1]
    except IndexError:
        actor_birth_soup = False
        print("Oops, Birth Date and Birth Place unknown!")
    if actor_birth_soup:
        # Checks whether there is a birth date, or throws exception
        try:
            actor_birth_date = actor_birth_soup.time.find_all("a")[0:2]
            actor_birth_dict["Birth Date: "] = actor_birth_date[0].string + ", " + actor_birth_date[1].string
            print("Birth Date is known! > " + actor_birth_dict["Birth Date: "])
        except:
            actor_birth_dict["Birth Date: "] = "Unknown (exception)"
            e = sys.exc_info()[0]
            write_to_page( "<p>Error: %s</p>" % e )

        # Checks whether there is a birth place, or throws exception
        try:
            actor_birth_place_link = actor_birth_soup.find_all("a")[2]
            # Checks whether the link above refers to birth place or not
            if "birth_place" in str(actor_birth_place_link):
                print("Birth place is known! > " + actor_birth_place_link.string)
                actor_birth_place = actor_birth_place_link.string
                actor_birth_dict["Actor Birth Place: "] = actor_birth_place
            else:
                actor_birth_dict["Actor Birth Place: "] = "Unknown (no place, no date)"
                print("Birth place is unknown! :'(")
        except:
            actor_birth_dict["Actor Birth Place: "] = "Unknown (exception)"
            e = sys.exc_info()[0]
            write_to_page( "<p>Error: %s</p>" % e )

        return actor_birth_dict
        
    else:
        return {"Birth Date: " : "Unknown (soup)", "Actor Birth Place: " : "Unknown (soup)"}

# Function that scrapes all information about movies and its cast
# through a list of search terms
# Returns a list of movie objects
# These movie objects include a list of cast member dictionaries,
# which contain information about the respective cast member
def GetAllInformation(search_term_list, amount_results):

    end_results = []

    for search_term in search_term_list:
        search_term_results = {}
        search_results_list = GetMovieList(search_term, amount_results)
        print("Search Results List: " + str(search_results_list))

        for search_result in search_results_list:
            search_result_id = search_result['id']
            print("Search Result ID: " + search_result_id)
            cast_list = GetCastList(search_result['id'])
            search_term_results[search_result_id] = cast_list

        end_results.append(search_term_results)

    return end_results