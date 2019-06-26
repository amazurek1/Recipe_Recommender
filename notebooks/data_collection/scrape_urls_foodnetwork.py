from bs4 import BeautifulSoup
import requests
import time

# define cuisines
cuisines = ['american', 'asian', 'caribbean', 'chinese', 
            'french', 'indian', 'italian', 'japanese', 
            'mediterranean', 'mexican', 'middle-eastern', 
            'russian', 'spanish', 'thai', 'vegetarian']

# define range of pages to scrape
pages = range(1, 50)

# loop through list of cuisines
for cuisine in cuisines:

    # loop through pages
    for page in pages:

        # get data from web page
        recipes_page = requests.get('https://www.foodnetwork.com/search/{}-/p/{}/CUSTOM_FACET:RECIPE_FACET/rating'.format(cuisine, page))

        # parse through content on web page using Beautiful Soup
        soup = BeautifulSoup(recipes_page.content, 'html.parser')

        # collect all anchor tags
        tags = soup.find_all('h3', class_='m-MediaBlock__a-Headline')

        # pull out all urls from anchor tags
        urls = [tag.a.get('href') for tag in tags]

        print(urls)
        
        # write urls to txt file
        with open('./data/foodnetwork_urls.txt', 'a') as f:
            f.writelines('\n'.join(urls))
            f.writelines('\n')
            f.close()

            # print that the page has finished being scraped
            print('Page Done')
            print(cuisine, page)
        
        # pause after each hit
        time.sleep(60)
    
