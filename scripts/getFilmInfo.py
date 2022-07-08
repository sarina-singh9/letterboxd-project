import requests
from bs4 import BeautifulSoup as bs
import unicodedata
from collections.abc import Iterable

#https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

#used to format lists that may not be correct length
def formatList(list,limit):
    numItems=len(list)
    #do not need to cut or add items
    if (numItems==limit):
        return list
    #too many items
    if (numItems > limit):
        list=list[:limit]
    #empty genre spaces
    if (numItems < limit):
        for x in range(limit-numItems):
            list.append(" ")
    return list

def movieData(URL):
    #URL format: "https://letterboxd.com/film/tenet/"
    #should contain entire URL not only suffix
    r = requests.get(URL)
    soup = bs(r.content,'lxml')
    #year and title stored in same variable
    filmTitle = soup.select_one('[name="twitter:title"]')['content']
    filmYear= filmTitle[len(filmTitle)-5:len(filmTitle)-1]
    filmTitle=filmTitle[:len(filmTitle)-7]
    #can also be calculated from rating histogram, potentially delete
    avgRating = soup.select_one('[name="twitter:data2"]')['content']
    avgRating=avgRating[:len(avgRating)-9]
    #get languages spoken in film
    film_languages=[]
    language=soup.find('div',{'id':'tab-details'})
    children=language.select('div > p')[2].findChildren("a" , recursive=False)
    for child in children:
        film_languages.append(child.getText())
    #limit 3 languages
    film_languages=formatList(film_languages,4)
    #country that film is produced in
    film_countries=[]
    language=soup.find('div',{'id':'tab-details'})
    children=language.select('div > p')[1].findChildren("a" , recursive=False)
    for child in children:
        film_countries.append(child.getText())
    #limit 3 countries
    film_countries=formatList(film_countries,4)
    #film length
    length=soup.find('p',{'class':'text-link text-footer'}).getText()
    length=int(length.split('mins',1)[0])
    #genre list; num genres varies based on film
    film_genres=[]
    #https://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautifulsoup
    genres = soup.find('div', {'class': 'text-sluglist capitalize'}).p
    children = genres.findChildren("a" , recursive=False)
    for child in children:
        film_genres.append(child.getText())
    #limit 4 genres; add blank spaces for formatting reasons
    film_genres=formatList(film_genres,4)
    #rating histogram stored in different URL
    film_URL= URL.split(".com/",1)[1]
    r = requests.get("https://letterboxd.com/csi/"+film_URL+"rating-histogram/")
    soup=bs(r.content,'lxml')
    try:
        numFans=soup.find('a',{'class':'all-link more-link'}).getText()
    except:
        numFans=0
    #list for ratings histogram [# rated .5, # rated 1, ..., # rated 4.5, # rated 5]
    ratings=[]
    ratings_data=soup.find_all('li',{'class':'rating-histogram-bar'})
    for rating in ratings_data:
        ratings.append(unicodedata.normalize("NFKD",rating.a.get('title')))
    #calc all ratings for measure of popularity
    sumRatings=0
    for x in range(10):
        ratings[x]=int(ratings[x].split(' ',1)[0].replace(',', ''))
        sumRatings = sumRatings + ratings[x]
    #store all vars in one list to export to Excel
    movieInfo=[filmTitle,filmYear,length,film_genres,film_languages, film_countries,sumRatings,numFans,avgRating,ratings]
    return(list(flatten(movieInfo)))
