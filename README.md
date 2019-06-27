# Are You Hungry? - A Recipe Recommender System

The aim of this project was to create a content-based recipe recommender system with a SQL database backend and a front-end user interface which takes in input of ingredients from selected recipes and returns recommendations of recipes which are similar to the selected recipes based on their ingredients.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Data Collection](#data-collection)
3. [SQL Database](#database)
4. [Exploratory Data Analysis](#exploratory-data-analysis)
5. [Topic Modeling](#topic-modeling)
6. [Generating Recommendations](#generating-recommendations)
7. [Next Steps](#next-steps)
8. [Resources](#resources)

## Project Overview


## Data Collection

Recipes were webscraped using <a src="https://github.com/micahcochran/scrape-schema-recipe">scrape-schema-recipe</a>, a tool for scraping recipes into Python dictionaries, from Food Network (~ 6700 recipes) and Allrecipes (5000+ recipes). Currently, only the Food Network recipes are populated in the database and used in this project. However, recipes from Allrecipes will be added in the next iteration. To ensure there is a wide variety of recipes, Food Network recipes were scraped using international cuisine keywords such as: "american", "asian", "mexican", and "russian", while Allrecipes recipes were scraped from the first 200 pages of the World Cuisines section of the site.

After collection, the recipes were then cleaned, and separated into tables according to the database schema (discussed in the next section) before being loaded into the PostgreSQL database.

## SQL Database

## Exploratory Data Analysis (EDA)

## Topic Modeling

## Generating Recommendations

## Next Steps

<b><u>Improve Model</u>:</b>
* Additional data cleaning to remove more common ingredients from the model (add them to stopwords)
* Add recipe instructions to the model
* Add more recipes

<b><u>Improve User Interface</u>:</b>
* Improve website UI
* Add input text field - with more data, raw text can be input to generate recommendations

<b><u>Additional Iterations</u>:</b>
* Consider dietary restrictions/preferences and nutrition in the recommendations
    * Add flavor compounds data
    * Add nutrition data of each recipe
* Create a dynamic recommender system in which as user selects a recommended recipe, it is added to the list of selected recipes to trigger a new set of recommendations

## Resources

* <b>Analyzing Recipe Ingredients with LDA:</b> https://medium.com/@sallygao/analyzing-recipe-ingredients-with-latent-dirichlet-allocation-dba49b72d1b9
* <b>Article recommender:</b> https://github.com/kb22/Article-Recommender
* <b>LDA in Python:</b> https://www.machinelearningplus.com/nlp/topic-modeling-python-sklearn-examples/
* <b>Topic Modeling in Python with Gensim:</b> https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/