import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

NUMBER_OF_DAYS = 30
countOfNews = 0

def create_dataset_file():
    print("Creating Raw File")
    file = open('DawnNews.csv', "w+")
    file.write("Date,Link,Heading,Body\n")
    file.close()

def save_raw_news_to_dataset(date, link, heading, body):
    news = str(date) + "," + str(link) + "," + str(heading) + "," + str(body)
    file = open('DawnNews.csv', "a")
    file.write(news + "\n")
    file.close()


create_dataset_file()
now = datetime.datetime.now()

for i in range(1,NUMBER_OF_DAYS):
    #calculate the date 30 days before
    date = now - datetime.timedelta(days= i)

    #construct the url for scraping
    url = "https://www.dawn.com/archive/latest-news/{0}-{1}-{2}/".format(date.year,
                                                            date.month,
                                                            date.day)
    print("Archive News URL:", url)
    #request the web page
    resp = requests.get(url)

    #parse the page using beautifulsoup
    soup = BeautifulSoup(resp.text, 'html.parser')

    #find all the links present in the page
    links = soup.find_all('a')

    #iterate through the links and find the ones which are related to politics
    for link in links:
        
        try:
            if len(link['href']) > 70 and "dawn.com" in link['href']:
                try:      
                    news_url = link['href']
                    #make request for the news page
                    resp = requests.get(news_url)
                    #parse the page using beautiful soup
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    #find the div which contains the news body
                    news_body = soup.find('div', {'class': 'story__content'})
                    #print the news body
                    dateNews = str(date.strftime("%d/%m/%Y"))
                    newslink = str(news_url)
                    newsheading = str(link.text)
                    newsbody = str(news_body.text)

                    print("-----")
                    print("Date: ", dateNews)
                    print("Link: ", newslink)
                    # print("Heading: " ,newsheading)
                    # print("Body: ", newsbody)

                    # #### 
                    # # newsbody = ""
                    # # save_raw_news_to_dataset(dateNews, link, newsheading, newsbody)
                    # df=pd.DataFrame()
                    # df['Date']=dateNews
                    # df.T.to_csv('test.csv',mode='a',index=False,header=False)
                    countOfNews += 1
                    print("News Count: ", countOfNews)

                    
                    
                except:
                    pass
        except:
            pass