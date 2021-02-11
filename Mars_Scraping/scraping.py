# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
import time


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver.exe", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_url(browser):
    #Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #Scrape website for hemisphere image urls and titles
    html_hemispheres = browser.html
    hemisphere_soup_partial = soup(html_hemispheres, 'lxml')

    #Store main url
    main_url ="https://astrogeology.usgs.gov"

    img_list = hemisphere_soup_partial.find_all('div', class_='item')

    #Create list
    hemisphere_image_urls = []

    #Write code to retrieve the image urls and titles for each hemisphere.

    # For Loop to retrieve the full-resolution image URL and title for each hemisphere image?
    for img in img_list:
        hemisphere_dict = {}
        
        href = img.find('a', class_='itemLink product-item')
        link = main_url + href['href']
        browser.visit(link)
        
        time.sleep(1)
        
        hemisphere_html_full = browser.html
        hemisphere_soup_full = soup(hemisphere_html_full, 'lxml')
        
        img_title = hemisphere_soup_full.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
        
        img_url = hemisphere_soup_full.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
        
        # Append dictionary to list
        hemisphere_image_urls.append(hemisphere_dict)
        
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())