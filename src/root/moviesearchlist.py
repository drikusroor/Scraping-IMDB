'''
Created on 13 aug. 2015

@author: Ultra Patser
'''

import urllib3
from bs4 import BeautifulSoup
import json

http = urllib3.PoolManager()

def GetHtml(url):
    r = http.request('GET', url)
    return r.data

def GetMovieList(search_term):
    #url_example = "http://www.imdb.com/find?ref_=nv_sr_fn&q=titanic&s=all"
    domain = 'http://www.imdb.com/'
    url_first = 'find?q='
    #url_middle = '/classement/bloc-classement-page/'
    url_last_optional = '&s=tt&ttype=ft&ref_=fn_ft'
    search_url = domain + url_first + search_term + url_last_optional
    movie_list_html = GetHtml(search_url)
    movie_list_soup = BeautifulSoup(movie_list_html, 'html.parser')
    print(search_url)
    movie_list = []

    for row in movie_list_soup.table.find_all('tr'):
        movie_meta = {}

        for cell in row.find_all('td', class_='result_text'):
            movie_meta['url'] = cell.a.get('href')
            url = movie_meta['url']
            movie_meta['id'] = url[7: 16]
            movie_meta['name'] = cell.a.string
            cell.a.extract()
            year = cell.contents[1]
            movie_meta['year'] = year[2:6]
            movie_list.append(movie_meta)

    return movie_list

def GetActorList(movie_id):
    domain = 'http://www.imdb.com/'
    url_first = 'title/'
    url_middle = movie_id
    url_last = '/fullcredits?ref_=tt_cl_sm#cast'
    search_url = domain + url_first + url_middle + url_last
    print(search_url)
    actor_info_html = GetHtml(search_url)
    actor_info_soup = BeautifulSoup(actor_info_html, 'html.parser')
    return actor_info_soup

titanic_list = GetMovieList("daddy")
titanic_url = titanic_list[0]

for movie in titanic_list:
    print(movie)

print(titanic_url['id'])

soup = GetActorList(titanic_url['id'])

print(soup.prettify())