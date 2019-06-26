import json
import re
import ast
from isodate import parse_duration

# with open('./data/allrecipes_recipes3.json', 'r') as f:
#     data = json.load(f)

def transform_time(recipe):
    time_keys = ["cookTime", "prepTime", "totalTime"]
    for key in time_keys:
        try:
            recipe[key] = str(parse_duration(recipe[key]))
        except:
            recipe[key] = None

def transform_steps(recipe):
    try:
        recipe["recipeInstructions"] = re.sub("(\\n\\s+)", "", recipe["recipeInstructions"]).split(".")
        recipe["recipeInstructions"] = [step.strip(" ") for step in recipe["recipeInstructions"]]
    except:
        recipe["recipeInstructions"] = recipe["recipeInstructions"]

def transform_aggregate_review(recipe):
    aggregate_keys = ["ratingValue", "reviewCount"]
    for key in aggregate_keys:
        try:
            recipe["aggregateRating"]["properties"][key] = ast.literal_eval(recipe["aggregateRating"]["properties"][key])
        except:
            recipe["aggregateRating"]["properties"][key] = None

def transform_individual_review(recipe):
    reviews = recipe["review"]
    for review in reviews:
        try:
            review["properties"]["reviewRating"]["properties"]["ratingValue"] = ast.literal_eval(review["properties"]["reviewRating"]["properties"]["ratingValue"])
        except:
            review["properties"]["reviewRating"]["properties"]["ratingValue"] = None
