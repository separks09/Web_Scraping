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
    # create mars_data dict that we can insert into mongo
    mars_data = {}

    # visit first url
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
    # add items to mars_data
    mars_data["news_image"] = news_image_url
    mars_data["news_title"] = news_title
    mars_data["news_text"] = news_text

    # visit second url
    weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather)
    
    html = browser.html
    # create soup object from html
    soup3 = BeautifulSoup(html, 'html.parser')
    mars_weather = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #add items to mars_data
    mars_data["weather"] = mars_weather

    # visit thrid url
    featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured)
    # Create a Beautiful Soup object for jpl.nasa.gov
    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    featured_image = soup2.find("a", class_="button")["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov"+featured_image
    # Add items to mars_data
    mars_data["featured_image"] = featured_image_url

   # URL for fifth page to be scraped
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Set browser
    browser.visit(hemisphere_url)
    # Create a Beautiful Soup object from usgs.gov
    html = browser.html
    soup5 = BeautifulSoup(html, 'html.parser')
    # Find titles and images of Mars hemispheres from usgs.gov
    results3 = soup5.find_all("div", class_="item")
    # Iterate through results, storing dictionary items in list
    hemispheres = []
    for result in results3:
        # Store URL to full image in variable
        url = result.find("a")["href"].split("map")[-1]
        image_url = "https://astropedia.astrogeology.usgs.gov/download"+url+".tif/full.jpg"
        # Clean title and in variable
        title = (result.find("h3").text.split(" Enhanced")[0])
        # Create dictionary
        hemispheres_dict = {}
        # Store one instance of title and image
        hemispheres_dict["title"] = title
        hemispheres_dict["image_url"] = image_url
        # Add key and value to dict
        hemispheres_dict_values = hemispheres_dict
        # Append "entire" dict to list; dict is unordered and will overwrite on next iteration
        hemispheres.append(hemispheres_dict_values)
    # Add    
    mars_data["hemispheres"] = hemispheres

    return mars_data
