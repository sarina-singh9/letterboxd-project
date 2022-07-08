import random
import csv
import requests
from bs4 import BeautifulSoup as bs

#returns random film links (of numFilms quantity) from the
#first 'pages' pages of Letterboxd films sorted by popularity
def getFilmLinkAlt(pages, numFilms):
    #randomize page number, store in list of length numFilms
    #repetitions allowed
    #otherwise use random.sample
    #randint is INCLUSIVE of the max
    pageNos=[random.randint(0, pages) for x in range(numFilms)]
    #randomize film number, determines index returned
    #associated with equivalent index in pageNos list
    #70 films per page
    #repetition allowed
    #same number likely on different page
    #if not remove in postprocessing
    filmNos=[random.randint(0, 69) for x in range(numFilms)]
    #instantiate result list
    film_links=[]
    #iterate numFilms number of times
    for i in range(numFilms):
        #get content from appropriate page - will call numFilms # of pages
        if (pageNos[i]==0):
            r=requests.get('https://letterboxd.com/films/ajax/popular/size/small/')
        else:
            r=requests.get('https://letterboxd.com/films/ajax/popular/size/small/'+'page/'+str(pageNos[i]))
        soup = bs(r.content,'lxml')
        film_list=soup.find_all('div',{'data-component-class':"globals.comps.FilmPosterComponent"})
        film_links.append("https://letterboxd.com"+film_list[filmNos[i]]['data-film-link'])
    with open("filmsTest.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([film_links])         
    return

#ex: et 200 films from the first 115 pages of films
getFilmLinkAlt(115,200)
