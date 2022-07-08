from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import requests
import time
from urllib.request import urlopen
import unicodedata
import random
from getFilmInfo import movieData
from getLikes import getLikes
import csv
from itertools import chain
import copy

#this function doesnt get called as written
def getNumReviews(URL):
    r = requests.get(URL)
    soup = bs(r.text,"lxml")
    num_review_data=soup.find_all("a", {"class":"tooltip"})
   # print(num_review_data)
    return


#pass reviews URL page
def getProfileLinks(soup):
    profile_data = soup.find_all('strong',{'class':["name"]})
    profiles=[]
    for profile in profile_data:
        profiles.append('https://letterboxd.com'+profile.find("a")['href'])
    return(profiles)

#pass reviews URL page
def getComments(soup):
    comment_data = soup.find_all('span',{'class':["content-metadata"]})   
    comments=[]
    for comment in comment_data:
        curr_val=comment.find('a',{'class':["has-icon icon-comment icon-16 comment-count"]})
        if curr_val != None:
            comments.append(curr_val.getText())
        else:
            #No comments
            comments.append(0)
    return(comments)

#pass reviews URL page (data-film-link)
def getReviewText(URL):
    #only gets the text given the direct link to a review file
    r=requests.get(URL)
    text=""
    soup = bs(r.text,'lxml')
    #lose line spacing data
    #can record number of <p> tags for analysis
    numParagraphs=0
    for paragraph in soup.find_all('p'):
        text += " " + paragraph.text
        numParagraphs=numParagraphs+1
    return(text,numParagraphs)

#pass reviews URL page
def getReviewURLs(soup):
    reviews = soup.find_all('div',{'class':["body-text -prose collapsible-text"]})
    links=[]
    for review in reviews:
        links.append('https://letterboxd.com'+review.get("data-full-text-url"))        
    return(links)

#pass USER profile page
#slow, have to load each following page separately
def getFollowersFollowing(URL):
    r = requests.get(URL)
    soup = bs(r.text,"lxml")
    numFollowing =soup.find_all('span', {'class':['value']})[3].text
    numFollowers = soup.find_all('span', {'class':['value']})[4].text
    followingList = [numFollowing, numFollowers]
    return followingList

def getDates(soup):
    dates =soup.find_all('span', {'class':['_nobr']})
    date_list=[]
    for date in dates:
        #if date string is empty
        #need to get from child time tag with attribute 'datetime'
        if (not date.text):
            #date found in time tag in format yyyy-mm-dd
            #want in format dd-mmm, yyyy
            date=date.time['datetime'][:10]
            #print("date.text=",date.text)
            date_list.append(date)
           #some dates are nexted in time class 
        else:
            #else statement necessary
            #cannot access date.text in previous case
            date_list.append(date.text)
    return date_list

#goal:
#want a list of 12 lists with all associated info for each review sorted correctly
#(reviewText, numFollowers, numFollowing, numLikes, numComments,date)

#limit number of gets where possible
#in order to optimize code
def allReviewInfo(URL,i):
    all_review_info = [[] for x in range(12)]
    #scrape this data in order to use in all other functions
    r = requests.get(URL)
    soup = bs(r.text,"lxml")
    like_list=getLikes(URL)
    profile_links=getProfileLinks(soup)
    comment_list=getComments(soup)
    review_links=getReviewURLs(soup)
    date_links=getDates(soup)
    following_info=getFollowersFollowing(profile_links[i])
    review_info=getReviewText(review_links[i])
    var_list=[review_info[0],review_info[1],like_list[i],comment_list[i],following_info[0],following_info[1],date_links[i]]
    return var_list

#to write reviews into a CSV file
def writeRevCSV(rev_array,URL):
    film_data=movieData(URL)
    
    return


#called from scrapeReviewsWrapper()
#takes in URL of format
#'https://letterboxd.com/film/film-name/' exactly
#should match with result of getFilmLinks()
#takes in an int numReviews; how many reviews should be sampled
#from each film in the filmList
def scrapeReviews(URL,numReviews):
    getURL=URL + "reviews/by/activity"
    #need these requests in order to get the pageNumbers; will only run once per
    #function call
    r=requests.get(getURL)
    soup = bs(r.text,'lxml')
    #edit URL to be of form
    #"/film/film-title/reviews/"
    soupURL=URL.split(".com")[1]+ "reviews/"
    revString= soup.find('a',{'href':[soupURL]})['title']
    #correct improperly formatted data
    revString=unicodedata.normalize('NFKC',revString)
    #total number of Reviews - need in order to calculate # of pages of reviws
    numRevs=revString.split(" reviews")[0]
    #replace commas in # of reviews string in order to convert to int
    numRevs = numRevs.replace(',', '')
    totReviews=int(numRevs)
    #letterboxd only displays 128 pages of reviews maximum
    numRevs=min(128,int(numRevs))
    #12 pages of reviews
    totPages=int(int(numRevs)/12)
    #https://stackoverflow.com/questions/12759318/how-to-generate-unique-random-lists
    result = set()
    while len(result) < numReviews:     
        result.add((random.randint(0, 11),random.randint(0, totPages-1)))
    result=list(result)
    rev_array=[]
    for i in range(numReviews):
        #we are getting all the data but just taking the ith element
        #have to make the same number of page requests
        currFilm=result[i][0]
        currPage=result[i][1]
        rev_array.append(allReviewInfo(URL+"reviews/by/activity/page/"+str(currPage),currFilm))
    return rev_array

#reads in and writes to csvfile
#newFile boolean that tells if you are writing to new file or
#writing to existing file
def scrapeReviewsWrapper(csvPath,numReviews,newFile,start,end):
    #opens films stored in the csv input at csvPath
    with open(csvPath, newline='') as csvfile:
      reader = csv.reader(csvfile)
      #returns list of all films in your csv
      film_array = next(reader)
    #allows to only export certain films
    film_array=film_array[start:end]
    #writing result csv file
    #as written will either create new file
    #or append onto end if file already exists
    #will allow us to run code multiple times to get more data 
    with open('compiledData.csv','a',encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        #only write headers if the file is blank
        if (newFile==True):
            #write column headers     
            movieHeaders=["Film Title", "Film Year","Film Length","Genre 1","Genre 2","Genre 3","Genre 4","Language 1","Language 2","Language 3","Language 4","Country 1","Country 2","Country 3","Country 4","Total Ratings","Number of Fans","Average Ratings","0.5 Rating","1.0 Rating","1.5 Rating","2.0 Rating","2.5 Rating","3.0 Rating","3.5 Rating","4.0 Rating","4.5 Rating","5.0 Rating"]
            reviewHeaders=["Review Text","Number of Paragraphs","Number of Likes","Comments","Followers","Following","Date"]
            movieHeaders.extend(reviewHeaders)
            writer.writerow(movieHeaders)
        for film in film_array:
            #store basic data for each movie in row associated with that movie
            #prevent breaking out on individual cases
            movie_data=movieData(film)
            #returns review array with all desired info 
            #should not return from this call until all reviews from a certain film has been scraped
            review_data=scrapeReviews(film,numReviews)
            #review data is a list of lists
            #should be a numReviews length list containing lists
            #of reviews and relevant information
            for review in review_data:
                write_review=copy.deepcopy(movie_data)
                #tack review data onto associated film data
                write_review.extend(review)
                #write row to csv file (associated with one review)
                writer.writerow(write_review)
    return

#scrapeReviewsWrapper(csvPath,numReviews,newFile,start,end)
#ex: print 60 random reviews with headers from the first to third film listed in "filmsTest.csv"
#scrapeReviewsWrapper('filmsTest.csv',60,True,0,3)


