from bs4 import BeautifulSoup
import requests
import time


# define range of pages to scrape
pages = range(1, 200)

# loop through pages
for page in pages:

    # get data from web page
    recipes_page = requests.get('https://www.allrecipes.com/recipes/86/world-cuisine/?page={}'.format(page))

    # parse through content on web page using Beautiful Soup
    soup = BeautifulSoup(recipes_page.content, 'html.parser')

    # collect all anchor tags
    tags = soup.find_all('a', class_='fixed-recipe-card__title-link')

    # pull out all urls from anchor tags
    urls = [tag.get('href') for tag in tags]

    print(urls)
    
    # write urls to txt file
    with open('./data/allrecipes_urls.txt', 'a') as f:
        f.writelines('\n'.join(urls))
        f.writelines('\n')
        f.close()

        # print that the page has finished being scraped
        print('Page Done')
        print(page)
    
    # pause after each hit
    time.sleep(60)
    
