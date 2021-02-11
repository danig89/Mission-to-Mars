#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)


# # Visit the mars nasa news site

# In[3]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# ### Mars Weather

# In[15]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[16]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[17]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[18]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[19]:


# 2. Create a list to hold the images and titles.

#Scrape website for hemisphere image urls and titles
html_hemispheres = browser.html
hemisphere_soup_partial = soup(html_hemispheres, 'lxml')

#Store main url
main_url ="https://astrogeology.usgs.gov"

img_list = hemisphere_soup_partial.find_all('div', class_='item')

#Create list
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

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


# In[20]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[22]:


# 5. Quit the browser
browser.quit()

