import requests
from quopri import decodestring
from autoscraper import AutoScraper
import json
import unidecode


#scrape viewing IDs
#takes in a full review page
def getViewingList(URL):
    scraper = AutoScraper()
    scraper.load('viewing-counts')
    viewing_list=scraper.get_result_similar(URL)
    return(viewing_list)

#need Payload dictionary to send response
#takes list of viewing IDs
def writePayload(viewing_list):
    payload = {}
    payload['likeables']=viewing_list
    payload['likeCounts']=viewing_list
    return(payload)

#takes in list of dictionaries
#returns list of likes as ordered on the page
def orderLikes(viewing_list, likeables):
    like_list=[]
    #order counts by order of viewing ID in view test
    for viewingID in viewing_list:
        for likeable in likeables:
            curr_val=likeable['likeableUid']
            #find matching count
            if (likeable['likeableUid']==viewingID):
                #append appropriate list element
                #to extract the correct like count
                like_list.append(likeable['count'])
                #1:1 - once found stop looking
                break
    return(like_list)
    
def getLikes(URL):
    headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36','content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    session = requests.session()
    #assuming viewing list is in order displayed on the page
    viewing_list=getViewingList(URL)
    response_URL= 'https://letterboxd.com/ajax/letterboxd-metadata/'
    r = requests.post(response_URL, data=writePayload(viewing_list),headers=headers)
    response_data = json.loads(r.text)
    #returns list of dictionaries
    likeables = response_data.get('likeables')
    return(orderLikes(viewing_list,likeables))

print(getLikes('https://letterboxd.com/film/bone-tomahawk/reviews/by/activity/'))


