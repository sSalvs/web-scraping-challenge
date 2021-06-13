from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

######### NASA Mars News ##########
    # Visit redplanetscience.com/
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Create BeautifulSoup object
    html = browser.html
    soup = bs(browser.html, 'html.parser')
    
    # find the latest news title
    news_title = soup.find("div", class_="content_title").text

    # find the paragraph associated with the first title
    news_p = soup.find("div", class_="article_teaser_body").text




######### JPL MARS Space Image #########

    url_space_image = 'https://spaceimages-mars.com/'
    browser.visit(url_space_image )

    space_image_html = browser.html
    soup = bs(space_image_html, 'html.parser')


    # Find the featured image 
    for x in range(1):
        space_image_html = browser.html
        soup = bs(space_image_html, 'html.parser')
        relative_image_path = soup.find_all('a')[2]["href"]
        for reimage in relative_image_path:
            mars_image_url = soup.find_all('img')[1]["src"]
            featured_image_url = url_space_image + mars_image_url
        try:
            browser.links.find_by_partial_text(relative_image_path)
        except:
            print(error)



########## Mars Facts #########

    url_mars = 'https://galaxyfacts-mars.com'
    # view the table in df 
    tables = pd.read_html(url_mars)
    mars_facts_df = tables[0]
    # Rename the columns
    mars_facts_df.columns=["Info","Mars","Earth"]
   
    mars_facts_df.replace('\n', '')
    html_table = mars_facts_df.to_html(index=False)
    

   

#######  Mars Hemispheres #######

    # URL of page to be scraped
    hemisphere_url = 'https://marshemispheres.com'
    browser.visit(hemisphere_url)

    # Create BeautifulSoup object
    
    soup = bs(browser.html, 'html.parser')

    # Create list for image titles 
    title_list = []

    # find all image titles
    titles = soup.find_all('h3')


    for title in titles:
        title_list.append(title.text)
        
    # Drop 'back' from list  
    title_list = title_list[0:4]

    # create list to capture the space dictionary 

    space_image = []

    # loop through the hemisphere titles from the previous list to get image URL 

    for title in title_list:
        hemiphere_url = 'https://marshemispheres.com/'
        browser.visit(hemiphere_url)
        browser.click_link_by_partial_text(title)
        html = browser.html
        soup = bs(html, "html.parser")
        image_url = soup.find_all('li')[0].a["href"]
        space_image.append(image_url)
        print(image_url)



####### Create final space dictionary ##########

    space_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "relative_image_path": featured_image_url,
        "Table": html_table,
        "Cerberus_Hemisphere_Enhanced": title_list[0],
        "img_cerberus": hemiphere_url + space_image[0],
        "schiaparelli_enhanced": title_list[1], 
        "img_schiaparelli": hemiphere_url + space_image[1],
        "syrtis_enchanced": title_list[2], 
        "img_syrtis": hemiphere_url + space_image[2],
        "valles_enchanced": title_list[3], 
        "valles_img": hemiphere_url + space_image[3]}
           

  # Close the browser after scraping
    browser.quit()

    # Return results
    return space_dict
   
 
