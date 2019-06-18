import json
import pandas as pd
from stopwords import stop_words
from clean_data import get_ingredient_qty, get_ingredient_unit, get_ingredients
from config import USERNAME, PASSWORD, HOST_PORT, HOST_IP, DB_NAME
from sqlalchemy import create_engine
        
# define sqlalchemy engine to import/read data from sql db
engine=engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost:{HOST_PORT}/{DB_NAME}")

# read in data and assign to variable
ingredients = pd.read_json("data/foodnetwork_recipes5.json").reset_index()[["index", "name", "recipeIngredient"]]

# change index column to reflect recipe_id in db
ingredients.loc[:, "index"] = ingredients["index"].apply(lambda x: x+1)

# rename column names
ingredients.rename({"index":"recipe_id", "name": "title", "recipeIngredient": "ingredient_comment"}, axis=1, inplace=True)

# fill null values in ingredient column with unavailable to proceed to next step
ingredients.loc[ingredients.ingredient_comment.isnull()==True, "ingredient_comment"] = "unavailable"

# flatten ingredient series to multiple rows
ingredients_expand = pd.DataFrame(ingredients.ingredient_comment.tolist(), index=ingredients.recipe_id).stack().reset_index(name="ingredient_comment").drop("level_1", axis=1)

# pull out the ingredient quanitity
ingredients_expand["ingredient_qty"] = ingredients_expand["ingredient_comment"].apply(lambda x: get_ingredient_qty(x))

# pull out the ingredient unit
ingredients_expand["ingredient_unit"] = ingredients_expand["ingredient_comment"].apply(lambda x: get_ingredient_unit(x))

# pull out the ingredients
ingredients_expand["ingredient"] = ingredients_expand["ingredient_comment"].apply(lambda x: get_ingredients(x))

# replace underscore with spaces
ingredients_expand["ingredient"] = ingredients_expand["ingredient"].str.replace("_", " ")

# remove duplicates to prepare for sql upload
unique_ingredients = ingredients_expand[["recipe_id", "ingredient"]].drop_duplicates("ingredient")

# # import ingredients data into the ingredients table in sql db
# ingredients_expand["ingredient"].to_sql(name="ingredients", con=engine, schema="food", if_exists="append", index=False)

# read in ingredient_ids from importing ingredients data from sql
ingredients_sql = pd.read_sql_query("SELECT * FROM food.ingredients;", con=engine)

# merge ids to ingredients dataframe
ingredients_ids = ingredients_expand.merge(ingredients_sql, how="left", on="ingredient")

# # import ingredients data into the ingredients table in sql db
# ingredients_ids[["recipe_id", "ingredient_id", "ingredient_unit", "ingredient_qty", "ingredient_comment"]].to_sql(name="recipes_ingredients", con=engine, schema="food", if_exists="append", index=False)
