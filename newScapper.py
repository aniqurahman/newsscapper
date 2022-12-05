import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import csv
import re
from time import sleep

NUMBER_OF_DAYS = 200
countOfNews = 0

def create_dataset_file():
    print("Creating Raw File")
    # file = open('DawnNews.csv', "w+")
    # file.write("Date,Link,Heading,Body\n")
    # # Open the CSV file for writing
    with open('RAW_NEWS.csv', 'w+', newline='\n') as csvfile:
        writer = csv.writer(csvfile)

        # Write the data rows
        writer.writerow(["DateOfNews", "Topic", "LinkOfNews", "HeadingOfNews", "BodyOfNews"])
    csvfile.close()

def save_raw_news_to_dataset(date, rawTopic, link, heading, body):
    tokenTopic = re.split('/',rawTopic)
    topic = tokenTopic[4]
    with open('RAW_NEWS.csv', 'a', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, topic, link, heading, body])
    csvfile.close()


create_dataset_file()
now = datetime.datetime.now()

for i in range(1,NUMBER_OF_DAYS):
    #calculate the date 30 days before
    url = ""
    date = now - datetime.timedelta(days= i)
    dateOfNews = "{0:02d}-{1:02d}-{2:02d}".format(date.year, date.month,date.day)

    baseURLList =  [
                    "https://www.dawn.com/newspaper/national/",
                    "https://www.dawn.com/newspaper/business/", 
                    "https://www.dawn.com/newspaper/sport/"
                    ]

    for _indexBaseURL in range(0,len(baseURLList)):
        url = str(baseURLList[_indexBaseURL] + dateOfNews)
        print("Archive News URL: ", url)
        sleep(10)
        #request the web page
        resp = requests.get(url)
        print("Archive News Response: ", resp)
        if resp.status_code > 204:
            print("Archive News URL Not accessible!")
            #parse the page using beautifulsoup
        else:
            soup = BeautifulSoup(resp.text, 'html.parser')
            #find all the links present in the page
            links = soup.find_all('a')

            #iterate through the links and find the ones which are related to politics
            for link in links:
                try:
                    # if len(link['href']) > 70 and "dawn.com" in link['href'] and "#comments" not in link['href'] and "read full story" not in link['href']:
                    if len(link['href']) > 70 and "dawn.com" in link['href'] and "read full story" in link: 
                        try:      
                            news_url = link['href']
                            #make request for the news page
                            resp = requests.get(news_url)
                            #parse the page using beautiful soup
                            soup = BeautifulSoup(resp.text, 'html.parser')
                            
                            rawNewsheading = soup.find('title') 
                            newsheading = str(rawNewsheading.text)

                            #find the div which contains the news body
                            news_body = soup.find('div', {'class': 'story__content'})
                            #print the news body
                            dateNews = str(date.strftime("%d/%m/%Y"))
                            newslink = news_url
                            # newsheading = str(link.text)
                            newsbody = str(news_body.text)
                            # newsTopic = str(news_body.title)

                            print("-----")
                            print("Date: ", dateNews)
                            print("Link: ", newslink)
                            # print("Heading: " ,newsheading)
                            # print("Body: ", newsbody)

                            save_raw_news_to_dataset(dateNews, baseURLList[_indexBaseURL], link.attrs['href'], newsheading, newsbody)
                            
                            countOfNews += 1
                            print("News Count: ", countOfNews)
                            
                        except:
                            pass
                except:
                    pass