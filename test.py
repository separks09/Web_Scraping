import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": r"C:\Users\sharo\Desktop\ChromeDriver\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create surf_data dict that we can insert into mongo
    mars_data = {}

    # visit unsplash.com
    news= "https://mars.nasa.gov/news"
    browser.visit(news)
    time.sleep(2)

    html = browser.html
    # create a soup object from the html
    soup = BeautifulSoup(html, "html.parser")
    news_title = soup.find("div", class_="content_title").text.strip()
    news_text = soup.find("div", class_="article_teaser_body").text.strip()
    news_image = soup.find("div", class_="list_image").find("img")["src"]
    news_image_url = "https://mars.nasa.gov"+news_image

    time.sleep(2)
    # add our src to surf data with a key of src
    mars_data["news_image"] = news_image_url
    mars_data["news_title"] = news_title
    mars_data["news_text"] = news_text

    # visit surfline to get weather report
    weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather)
    # grab our new html from surfline
    html = browser.html
    # create soup object from html
    soup3 = BeautifulSoup(html, 'html.parser')
    mars_weather = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #add
    mars_data["weather"] = mars_weather

    # URL for second page to be scraped
    featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Set browser
    browser.visit(featured)
    # Create a Beautiful Soup object for jpl.nasa.gov
    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    featured_image = soup2.find("a", class_="button")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov"+featured_image
    # Add
    mars_data["featured_image"] = featured_image_url

    # URL for fourth page to be scraped
    facts = "https://space-facts.com/mars/"
    # Set browser
    browser.visit(facts)
    # Create a Beautiful Soup object for twitter.com
    html = browser.html
    soup4 = BeautifulSoup(html, 'html.parser')
    results = soup4.find_all("td", class_="column-1")
    results2 = soup4.find_all("td", class_="column-2")
    for result in results:
        
        facts_column.append(result.text.split(":")[0])
    for result in results2:
        results_column.append(result.text)
      
    return mars_data
