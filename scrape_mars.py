import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from time import sleep

def init_browser():
    executable_path = {'executable_path': 'C:/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape_info():
    browser = init_browser()
    sleep(2)
    #first site
    #############
    mars_site = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(mars_site)
    sleep(2)
    # Create BeautifulSoup object; parse with 'lxml'
    soup0 = BeautifulSoup(browser.html, 'lxml')
    news = soup0.find_all('li', class_='slide')
    title0 = news[0].find('div', class_='content_title').text
    body0 = news[0].find('div', class_="article_teaser_body").text
    print("Finished with Nasa")
    
    #######################
    # Get the average temps
    image_site = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_site)
    sleep(2)
    soup1 = BeautifulSoup(browser.html, 'lxml')
    image = soup1.find('section',class_='centered_text clearfix main_feature primary_media_feature single')
    picture_url = image.article['style'][23:-3]
    base_url = image_site.split('spaceimages')[0][:-1]
    image_url = base_url + picture_url
    print("Finished with Pictures")
    
    #######################
    weather_site = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_site)
    sleep(5)
    soup2 = BeautifulSoup(browser.html, 'lxml')
    weather = soup2.find('ol', class_='stream-items js-navigable-stream')
    try:
        mars_weather = weather.li.find("div", class_ = 'js-tweet-text-container').p
        mars_weather.find('a').extract()
        mars_weather= mars_weather.text
    except AttributeError:
        mars_weather = weather.li.find("div", class_ = 'js-tweet-text-container').p.text
    
    print("Finished with Twitter")
    ######################
    # Get the max avg temp
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    sleep(5)
    soup4 = BeautifulSoup(browser.html, 'lxml')
    facts = soup4.find('section', class_='sidebar widget-area clearfix')
    table_html = str(facts.table)
    # facts_url = "https://space-facts.com/mars/"
    # print(facts_url)
    # facts_df = pd.read_html(facts_url)[0]
    # print('furhter')
    # facts_df = facts_df[0]
    # html_table = facts_df.to_html()

    print("finished with pandas html")
    ##################################
    hemisphere_site = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_site)
    sleep(2)
    soup3 = BeautifulSoup(browser.html, 'lxml')
    hemi_div = soup3.find('div',class_='collapsible results').find_all('div',class_='item')
    hemi_list = [x.h3.text for x in hemi_div]
    dict_list = []
    for hemi in hemi_list:
        try:
            browser.visit(hemisphere_site)
            sleep(1)
            browser.click_link_by_partial_text(hemi)
            sleep(1)
            current_page = BeautifulSoup(browser.html, 'lxml')
            dict0 = {'title': hemi, 'img_url': current_page.ul.li.a['href']}
            dict_list.append(dict0)
        except Exception as e: print(f'Error: {e}')
    print("Finished with hemispheres")     
        
    # Store data in a dictionary
    mars_data = {
        "title": title0,
        "body_p": body0,
        "background_img": image_url,
        "tweet_text": mars_weather,
        "facts_table": table_html,
        "hemispheres": dict_list
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data