from format_recipes import transform_time, transform_steps, transform_aggregate_review, transform_individual_review
import scrape_schema_recipe
import time
import json

# read in the urls saved in text file into a list and assign to a variable
with open(r'./data/allrecipes_urls.txt') as f:
    urls = list(f.readlines())

# remove '\n' at end of each link and put in new list
urls_cleaned = [url.strip('\n') for url in urls]
# urls_subset = urls_cleaned[:5]

# initalize empty list to store recipes
recipes = []

# loop through list of cleaned urls
for url in urls_cleaned:

    try:
        # scrape url and obtain page information
        recipe_list = scrape_schema_recipe.scrape_url(url)

        # get relevant information out of the page
        recipe = recipe_list[0]
        
        # transform time duration
        transform_time(recipe)

        # transform steps in recipe instructions
        transform_steps(recipe)

        # transform the data type for aggregate review
        transform_aggregate_review(recipe)

        # transform the data type for individual review
        transform_individual_review(recipe)

        # add each recipe after scraping and transformations to list
        recipes.append(recipe)

        # print that the page has finished being scraped
        print('Page Done')
        print(url)

        # pause after each hit
        time.sleep(1.2)

    except Exception as e:
        
        # print Exception
        print(e)

# write data to json file
with open('./data/allrecipes_recipes5.json', 'w') as fr:
    json.dump(recipes, fr, sort_keys=True, indent=4)

# close file after writing in all data
fr.close()
