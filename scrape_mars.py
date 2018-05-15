from bs4 import BeautifulSoup as bs
from splinter import Browser
import pymongo
# URL of first page to be scraped
url = "https://mars.nasa.gov/news"
# Path to ChromeDriver\n",
executable_path = {'executable_path': r'C:\\Users\\sharo\\Desktop\\ChromeDriver\\chromedriver.exe'}
# Set browser\n",
browser = Browser("chrome", **executable_path, headless=False)
browser.visit(url)
# Create a Beautiful Soup object for nasa.gov\n",
html = browser.html
soup = bs(html, 'html.parser')

news_title = soup.find("div", class_="content_title").text.strip())
news_text = soup.find("div", class_="article_teaser_body").text.strip())
news_image = soup.find("div", class_="list_image").find("img")["src"]
news_image_url = "https://mars.nasa.gov"+news_image
# URL for second page to be scraped\n",
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
# Set browser
browser2 = Browser("chrome", **executable_path, headless=False)
browser2.visit(url2)
# Create a Beautiful Soup object for jpl.nasa.gov
html2 = browser2.html
soup2 = bs(html2, 'html.parser')
featured_image = soup2.find("a", class_="button")"data-fancybox-href"]
featured_image_url = "https://www.jpl.nasa.gov"+featured_image
# URL for third page to be scraped
url3 = "https://twitter.com/marswxreport?lang=en"
# Set browser
browser3 = Browser("chrome", **executable_path, headless=False)
browser3.visit(url3)
# Create a Beautiful Soup object for twitter.com
html3 = browser3.html
soup3 = bs(html3, 'html.parser')
mars_weather = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    "print(mars_weather)"
# URL for fourth page to be scraped
url4 = "https://space-facts.com/mars/"
# Set browser
browser4 = Browser("chrome", **executable_path, headless=False)
browser4.visit(url4)
# Create a Beautiful Soup object for twitter.com
html4 = browser4.html
soup4 = bs(html4, 'html.parser')
results = soup4.find_all("td", class_="column-1")
results2 = soup4.find_all("td", class_="column-2")
for result in results:
    facts_column.append(result.text.split(":")[0])
for result in results2:
    results_column.append(result.text)
data = {"Fact":facts_column, "Result": results_column}
facts_df = pd.DataFrame(data)
facts_df.to_html("mars_facts.html", index = False)
# URL for fifth page to be scraped
url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
# Set browser
browser5 = Browser("chrome", **executable_path, headless=False)
browser5.visit(url5)
# Create a Beautiful Soup object from usgs.gov
html5 = browser5.html
soup5 = bs(html5, 'html.parser')
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