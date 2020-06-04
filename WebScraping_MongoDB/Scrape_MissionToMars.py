# Import required libraries/dependencies

from splinter import Browser

from bs4 import BeautifulSoup

import pandas as pd

import time

import requests as req

import pprint as pp



def init_browser():

    # Invoke the chromedriver/browser for Windows

    # to read the html pages for scraping/parsing the data.

    executable_path = {'executable_path': 'chromedriver.exe'}

    return Browser('chrome', **executable_path, headless=False)



def scrape():

    # Scrape and return the data from the html pages

    browser = init_browser()



    # Create a Dictionary to store the information retrieved

    mars_dict = {}



###---------------------------- Visit NASA Mars site --------------------------

    nasa_url = 'https://mars.nasa.gov/news/'

    browser.visit(nasa_url)

    time.sleep(2)                               # Extra 2 secs for the page to load fully

    html = browser.html                         # HTML object

    soup = BeautifulSoup(html, 'html.parser')   # Parse HTML with BeautifulSoup



    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.

    # Use Beautiful Soup's find() method to navigate and retrieve news

    news = soup.find('div', class_='image_and_description_container')

    news_title = news.find('div', class_='content_title').find('a').text

    news_p = news.find('div', class_='article_teaser_body').text



    # Store the info in the mars_dict

    mars_dict['news_title'] = news_title

    mars_dict['news_p'] = news_p



###----------- Visit JPL Mars Space Images through splinter module ------------

    # This is a 3 step process

    jpl_url = 'https://www.jpl.nasa.gov'

    featured_page_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'



    # Invoke the chromebrowser to the 'featured_page_url' and get the html object to it

    browser.visit(featured_page_url)

    time.sleep(1)                               # Extra 1 sec for the page to load fully

    html = browser.html                         # HTML object

    soup = BeautifulSoup(html, 'html.parser')   # Parse HTML with BeautifulSoup



    # Get the url for the detailed image

    featured_url = soup.find('a', class_='button fancybox')['data-link']

    #print(featured_url)

    image_detail_url = jpl_url + featured_url



    # Use the URL from above to invoke the html page and extract the url for the Largeimage

    browser.visit(image_detail_url)

    time.sleep(1)                               # Extra 1 sec for the page to load fully

    html = browser.html                         # HTML object

    soup = BeautifulSoup(html, 'html.parser')   # Parse HTML with BeautifulSoup



    fullres_url = soup.find('article').find('figure', class_='lede').find('a')['href']

    featured_image_url = jpl_url + fullres_url



    # Store the info in the mars_dict

    mars_dict['featured_image_url'] = featured_image_url



###---------------- Visit the Mars Weather Twitter account --------------------

    # twitter account - https://twitter.com/marswxreport?lang=en here and scrape

    # the latest Mars weather tweet from the page. Save the tweet text for the

    # weather report as a variable called mars_weather.



    twitter_mars_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(twitter_mars_url)

    time.sleep(10)                              # Extra 10 secs for the page to load fully

    html = browser.html                         # HTML object

    soup = BeautifulSoup(html, 'html.parser')   # Parse HTML with BeautifulSoup



    # Parse HTML with Beautiful Soup for the html page returned from above.

    # Find all the tweets by 'div' and  class', then get the first tweet for

    # the latest weather info.



    tweets = soup.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')



    # Get the latest tweet and replace the new line ('\n') character with a

    # space (' ') character within the body of text.

    latest_tweet = tweets[0].find('span').text.replace('\n', ' ')

    # Adding <br> tag to allow for moe readable display of the weather in the web page

    latest_tweet = latest_tweet.replace(')', ')<br>')



    # Store the info in the mars_dict

    mars_dict['latest_tweet'] = latest_tweet



###--------------------- Visit the Mars Facts Webpage ------------------------

    # Visit the Mars Facts webpage here and use Pandas to scrape the table

    # containing facts about the planet including Diameter, Mass, etc.



    #Mars space facts url

    mars_facts_url = 'https://space-facts.com/mars/'



    #Use Pandas to scrape the planet profile

    mars_facts = pd.read_html(mars_facts_url)

    mars_facts_df = mars_facts[0]



    # Name the columns of the DataFrame

    mars_facts_df.columns = ['Fact', 'Detail']

    mars_facts_df.set_index('Fact', inplace=True)



    # Pandas Dataframe converted to html table

    mars_facts_table_html = mars_facts_df.to_html()

    # html version with new line charcaters removed.

    mars_facts_table_html = mars_facts_table_html.replace("\n", "")

    #mars_facts_table_html



    # Store the info in the mars_dict

    mars_dict['mars_facts_table_html'] = mars_facts_table_html



###----------------------------- Mars Hemispheres ----------------------------

    # * Visit the USGS Astrogeology site

    # * (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

    # * to obtain high resolution images for each of Mar's hemispheres.

    # * You will need to click each of the links to the hemispheres in order

    # * to find the image url to the full resolution image. Save both the image

    # * url string for the full resolution hemisphere image, and the Hemisphere

    # * title containing the hemisphere name. Use a Python dictionary to store

    # * the data using the keys img_url and title.

    # * Append the dictionary with the image url string and the hemisphere

    # * title to a list. This list will contain one dictionary for each hemisphere.

    #

    # Example:

    # ```

    # hemisphere_image_urls = [

    # {"title": "Valles Marineris Hemisphere", "img_url": "..."},

    # {"title": "Cerberus Hemisphere", "img_url": "..."},

    # {"title": "Schiaparelli Hemisphere", "img_url": "..."},

    # {"title": "Syrtis Major Hemisphere", "img_url": "..."},

    # ]

    # ```



    # Visit hemispheres website through splinter module

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)



    time.sleep(2)                               # Extra 2 secs for the page to load fully

    html = browser.html                         # HTML object

    soup = BeautifulSoup(html, 'html.parser')   # Parse HTML with BeautifulSoup



    # Retreive all items that contain mars hemispheres information

    items_list = soup.find_all('div', class_='item')



    # Store the base url

    hemispheres_base_url = 'https://astrogeology.usgs.gov'



    hemispheres_image_urls = []     # Create empty list for hemisphere urls

    # Loop through the items_list retrived in teh previous step

    for i in items_list:

        title = i.find('h3').text       # Store title

        # Store link that leads to full image website

        partial_img_url = i.find('a', class_='itemLink product-item')['href']



        # Visit the link that contains the full image website

        browser.visit(hemispheres_base_url + partial_img_url)

        html = browser.html                         # HTML object

        soup = BeautifulSoup(html, 'html.parser')   # Parse HTML with BeautifulSoup



        # Retrieve full image source

        img_url = hemispheres_base_url + soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries

        hemispheres_image_urls.append({'title' : title, 'img_url' : img_url})

       # Store the info in the mars_dict

    mars_dict['hemispheres_image_urls'] = hemispheres_image_urls

     #Quit the browser before exiting the application

    browser.quit()

# Return results

    return mars_dict

