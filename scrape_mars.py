# MongoDB and Flask Application

from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time 



# coding: utf-8

#Site Navigation
executable_path = {"executable_path": r"C:\Users\arkha\Desktop\bootcamp\nu-chi-data-pt-02-2020-u-c\Homework\12-Web-Scraping-and-Document-Databases\Instructions\chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape & dictionary
def scrape():
    newstitle = marsnews()
    

    final_data = {
    "news_title": newstitle[0], 
    "news_text": newstitle[1],
    "mars_image": marsimage(),
    "mars_weather": marsweather(),
    # "mars_data": marsfacts(),
    "mars_hemisphere": marshemispheres()}

    return final_data

# Mars News

def marsnews():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_text = soup.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_text]
    return output

# JPL Mars Space Images - Featured Image
def marsimage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# Mars Weather
def marsweather():
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    pattern = re.compile(r'sol')
    mars_weather = soup.find('span', text=pattern).text
    return(mars_weather)

    

# Mars Facts
def marsfacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(index = False, header = False)
    return mars_facts


# Mars Hemispheres
def marshemispheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere


