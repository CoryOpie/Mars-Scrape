#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests


# ## NASA Mars News

# In[2]:
def init_browser():
    executable_path = {"executable_path" : "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    #path
    # executable_path = {"executable_path": "chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)

    browser = init_browser()

    # In[3]:


    #set up url
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    time.sleep(2)

    # In[4]:


    #scrape html and find item in list
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, "html.parser")
    nasa_results = nasa_soup.find("ul", class_="item_list")

    # print(nasa_results)


    # In[5]:


    news_title = nasa_results.find("div", class_="content_title").text
    news_teaser = nasa_results.find("div", class_="article_teaser_body").text

    # print(news_title)
    # print(news_teaser)
    # browser.quit()


    # ## JPL Mars Space Images - Featured Image

    # In[37]:


    #path
    # executable_path = {"executable_path": "chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)


    #url

    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    jpl_url_root = jpl_url.split("index.html")[0]
    browser.visit(jpl_url)

    time.sleep(1)
    # In[38]:


    #click image link
    browser.links.find_by_partial_text("FULL")
    time.sleep(5)


    # In[39]:


    #find image url

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")
    # jpl_image = jpl_soup.find("div", class_="fancybox-skin")

    jpl_image = jpl_soup.find_all("img")[1]["src"]
    # print(jpl_image)

    # browser.quit()

    featured_image_url = jpl_url_root + jpl_image
    # print(featured_image_url)
    # https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg


    # ## Mars Facts

    # In[12]:


    #path/url

    # executable_path = {"executable_path": "chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)

    #to table
    facts_df = pd.read_html(facts_url)

    # print(facts_df)
    # browser.quit()


    # In[33]:


    # type(facts_df)

    new_df = facts_df[0]

    new_df.columns = ["Description", "Information"]

    new_df.set_index("Description", inplace=True)



    # new_df.head(20)


    # In[34]:


    # facts_table = new_df.to_html()

    newnew_df = new_df.to_html()

    # print(facts_table)


    # ## Mars Hemispheres

    # In[8]:


    # executable_path = {"executable_path": "chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemi_url_root = hemi_url.split("/search")[0]
    browser.visit(hemi_url)
    time.sleep(2)

    # In[9]:


    title_list = []
    url_list = []

    #scrape site and get each hemisphere page
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, "html.parser")
    hemi_results = hemi_soup.find_all("div", class_="item")
    time.sleep(2)
    #get url for each hemisphere
    for item in hemi_results:
        item_url = item.a["href"]
        item_full_url = hemi_url_root + item_url
        url_list.append(item_full_url)
        title = item.find("h3").text
        title_list.append(title)

    # print(item_full_url)
    # print(title_list)


    # In[10]:


    #Get image url from each page and create url list

    url_dict_list = []


    for item_url in url_list:
        browser.visit(item_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        img_path = soup.select_one("ul")
        image_url = img_path.a["href"]
        url_dict_list.append(image_url)

    # print(url_dict_list)


    # In[11]:


    # combine 2 lists to get one list of dictionaries

    hemisphere_image_urls = []

    for url, title in zip(url_dict_list, title_list):
        hemisphere_image_dict = {}
        hemisphere_image_dict["title"] = title
        hemisphere_image_dict["img_url"] = url
        hemisphere_image_urls.append(hemisphere_image_dict)
        
    # print(hemisphere_image_urls)


    # browser.quit()

    mars_data_dict = {
        "news_title" : news_title,
        "news_teaser" : news_teaser,
        "mars_facts" : newnew_df,
        "featured_image_url" : featured_image_url,
        "hemisphere_image" : hemisphere_image_urls
    }

    browser.quit()
    return(mars_data_dict)



# In[4]:


# get_ipython().system('jupyter nbconvert --to script scrape_mars.py')


# In[ ]:




