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

Recipes were webscraped from Food Network (~ 6700 recipes) and Allrecipes (5000+ recipes). Currently, only the Food Network recipes are populated in the database and used in this project. However, recipes from Allrecipes will be added in the next iteration. To ensure there is a wide variety of recipes, Food Network recipes were scraped using international cuisine keywords such as: "american", "asian", "mexican", and "russian", while Allrecipes recipes were scraped from the first 200 pages of the World Cuisines section of the site.

After collection, the recipes were then cleaned, and separated into tables according to the database schema (discussed in the next section) before being loaded into the PostgreSQL database.

## SQL Database

## Exploratory Data Analysis (EDA)

## Topic Modeling

## Generating Recommendations

## Next Steps

## Resources