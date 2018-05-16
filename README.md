

```python
# Import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
```


```python
# URL of first page to be scraped
url = "https://mars.nasa.gov/news"

# Path to ChromeDriver
executable_path = {'executable_path': r'C:\Users\sharo\Desktop\ChromeDriver\chromedriver.exe'}

# Set browser
browser = Browser("chrome", **executable_path, headless=False)
browser.visit(url)

# Create a Beautiful Soup object for nasa.gov
html = browser.html
soup = bs(html, 'html.parser')
```


```python
news_title = soup.find("div", class_="content_title").text.strip()
news_text = soup.find("div", class_="article_teaser_body").text.strip()
news_image = soup.find("div", class_="list_image").find("img")["src"]
news_image_url = "https://mars.nasa.gov"+news_image

print(news_title)
print(news_text)
print(news_image_url)
```

    Mars Helicopter to Fly on NASA’s Next Red Planet Rover Mission
    NASA is adding a Mars helicopter to the agency’s next mission to the Red Planet, Mars 2020.
    https://mars.nasa.gov/system/news_items/list_view_images/8335_helicopter20180511-16-th.jpg
    


```python
# URL for second page to be scraped
url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

# Set browser
browser2 = Browser("chrome", **executable_path, headless=False)
browser2.visit(url2)

# Create a Beautiful Soup object for jpl.nasa.gov
html2 = browser2.html
soup2 = bs(html2, 'html.parser')
```


```python
featured_image = soup2.find("a", class_="button")["data-fancybox-href"]
featured_image_url = "https://www.jpl.nasa.gov"+featured_image

print(featured_image_url)
```

    https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19180_ip.jpg
    


```python
# URL for third page to be scraped
url3 = "https://twitter.com/marswxreport?lang=en"

# Set browser
browser3 = Browser("chrome", **executable_path, headless=False)
browser3.visit(url3)

# Create a Beautiful Soup object for twitter.com
html3 = browser3.html
soup3 = bs(html3, 'html.parser')
```


```python
mars_weather = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)
```

    Sol 2050 (May 13, 2018), Sunny, high 1C/33F, low -71C/-95F, pressure at 7.37 hPa, daylight 05:21-17:20
    


```python
# URL for fourth page to be scraped
url4 = "https://space-facts.com/mars/"

# Set browser
browser4 = Browser("chrome", **executable_path, headless=False)
browser4.visit(url4)

# Create a Beautiful Soup object for twitter.com
html4 = browser4.html
soup4 = bs(html4, 'html.parser')
```


```python
results = soup4.find_all("td", class_="column-1")
results2 = soup4.find_all("td", class_="column-2")
```


```python
facts_column = []
results_column = []

for result in results:
    facts_column.append(result.text.split(":")[0])


for result in results2:
    results_column.append(result.text)
    
data = {"Fact":facts_column, "Result": results_column}
facts_df = pd.DataFrame(data)

facts_df.to_html("mars_facts.html", index = False)

facts_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Fact</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter</td>
      <td>6,792 km\n</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter</td>
      <td>6,752 km\n</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period</td>
      <td>687 days (1.9 years)\n</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
# URL for fifth page to be scraped
url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

# Set browser
browser5 = Browser("chrome", **executable_path, headless=False)
browser5.visit(url5)

# Create a Beautiful Soup object from usgs.gov
html5 = browser5.html
soup5 = bs(html5, 'html.parser')
```


```python
# Find titles and images of Mars hemispheres from usgs.gov
results3 = soup5.find_all("div", class_="item")
```


```python
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
    
hemispheres
```




    [{'title': 'Cerberus Hemisphere',
      'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
     {'title': 'Schiaparelli Hemisphere',
      'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
     {'title': 'Syrtis Major Hemisphere',
      'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
     {'title': 'Valles Marineris Hemisphere',
      'image_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]


