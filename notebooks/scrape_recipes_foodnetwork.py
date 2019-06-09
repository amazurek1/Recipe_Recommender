import scrape_schema_recipe
from format_recipes import transform_time
import time
import json

# read in the urls saved in text file and assign to a variable
with open(r'./data/foodnetwork_urls.txt') as f:
    urls = list(f.readlines())

# create a new list with cleaned urls - add https:// and strip '//' and '\n' from each url
urls_cleaned = ['https:' + url.strip('\n') for url in urls]
# urls_subset = urls_cleaned[:5]

# initialize an empty list to contain recipes
recipes = []

# loop through list of cleaned urls
for url in urls_cleaned:

    try:

        # scrape url and obtain page information
        recipe_list = scrape_schema_recipe.scrape(url)

        # get relevant information out of the page
        recipe = recipe_list[0]
        # print('Recipe: \n', recipe)

        # transform the time values to a string of the total time of the recipes
        transform_time(recipe)

        # add recipe to list of recipes
        recipes.append(recipe)

        # print that the page has finished being scraped
        print('Page Done')
        print(url)

        # pause after each hit
        time.sleep(1)

    except Exception as e:
        
        # print Exception
        print(e)

# write data to json file
with open('./data/foodnetwork_recipes5.json', 'w') as fr:
    json.dump(recipes, fr, sort_keys=True, indent=4)

# close file after writing
fr.close()
