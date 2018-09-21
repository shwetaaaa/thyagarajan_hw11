from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import requests

# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Function to scrape for Mars
def scrape_mars():
    
    # Initialize browser
    browser = init_browser()
    
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    
    # results are returned as an iterable list
    news = soup.find('div', class_='content_title')
    mars_news_title=news.a.text
    
    news_p = soup.find('div', class_='article_teaser_body')
    news_paragraph=news_p.text
    
    #JPL Mars Space Images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    soup

    item_list = soup.find("ul", class_="articles")
    item_list
    articles = item_list.find_all('li', class_='slide')
    articles
    images = []
    
    for article in articles:
       link = article.find('a')
       news_title = link["data-title"]
       news_link = "https://www.jpl.nasa.gov" + link["data-link"]
       news_image = "https://www.jpl.nasa.gov" + link["data-fancybox-href"]
       news_description = link["data-description"]
       images.append({
           "news_title":news_title,
           "news_link":news_link,
           "news_image":news_image,
           "news_description":news_description
       })
    featured_image_url=images[0]['news_image']
    
    #Mars Weather
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    mars_weather=soup.find('div',class_='js-tweet-text-container').p.text
    
    #Mars Facts
    import pandas as pd
    url='http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=tables[0]
    df.columns=['Fact','Value']

    # convert the data to a HTML table string.
    fact_table = df.to_html()
    fact_table.replace('\n', '')
    df.to_html('fact_table.html')
    
    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/resultsq=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    hemisphere_image_urls=[]
    click_text=soup.find_all('div',class_='description')
    for items in click_text:
        image_links=items.find_all('a')
        text=image_links[0].h3.text
        browser.click_link_by_partial_text(text)
        current_page_html=browser.html
        soup = BeautifulSoup(current_page_html, 'lxml')
        title=soup.find_all('section',class_='block')[0].h2.text
        url=soup.find_all('img',class_='wide-image')[0]
        image_url='https://astrogeology.usgs.gov'+url['src']
        image_dict={}
        image_dict['Title']=title
        image_dict['Image_URL']=image_url
        hemisphere_image_urls.append(image_dict)
        browser.back()
        
    #Dictionary    
    mars = {
            "news_title": mars_news_title,
            "news_para": news_paragraph,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "mars_facts": fact_table,
            "mars_hemispheres": hemisphere_image_urls
    }
    # Return results
    return mars
    