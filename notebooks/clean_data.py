import re
import string
import pandas as pd
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer, PorterStemmer
from stopwords import stop_words


# create function to pull out the ingredient quantity
def get_ingredient_qty(ingredient):
    # remove all text between parentheses ingredients
    cleaned = re.sub(r"([(][^(]+[$)])", "", ingredient)
    # remove punctuation
    cleaned = re.sub("[%s]" % re.escape("!|#|$|%|&|'|(|)|*|+|,|-|.|:|;|<|=|>|?|@|[|]|^|_|`|{|}|~"), "", cleaned)
    # define pattern to match with input
    m = re.match(r"((?:\d+.)?\d+(?:.\d+\s?\.?)?)", cleaned)
    # set condition that if there is a match return it, else nothing
    if m:
        return m.group(1)
    else:
        return None

def get_ingredient_unit(ingredient):
    # define list of units
    units = ["tablespoon", "tbsp", "tbs", "tbl", "teaspoon", "tsp", "teaspoons", "ounce", "ounces", "fluid ounce", 
            "fluid ounces", "oz", "fluid oz", "fl oz", "gill", "cup", "c", "C", "pint", "pt", "fluid pint", "pints", "fluid pints"
            "fl pt", "quart", "qt", "fluid quart", "fl qt", "gallon", "liter", "litre", "L", "milliliter", "milliliters"
            "millilitre", "mL", "ml", "deciliter", "dl", "dL", "decilitre", "gallon", "gal", "gallons", "gram", "gramme", "g", "grams"
            "pound", "lb", "pounds", "milligram", "mg", "decigram", "dg", "kilogram", "kg", "kilogramme", "kilograms" 
            "millimeter", "millimetre", "mm", "decimeter", "decimetre", "dm", "meter", "metre", "m", "kilometer", "kilometre", "kilo", "km", 
            "centimeter", "centimetre", "cm", "inch", "in", "cubic meter", "cm3", "m3", "mm3", "km3", "celsius", "Celsius", "Fahrenheit", "F", 
            "pinch", "handful", "loaf", "dash", "Dash", "stick", "head", "bag", "bags", "package", "packages", "envelope", "drizzle"]
    # remove all text between parentheses ingredients
    parsed = re.sub("([(][^(]+[$)])", "", ingredient)
    # remove the quantities
    parsed = re.sub(r"^(\d*\/?\d?\s?\d?\/?\d?)", " ", parsed)
    # remove punctuation
    parsed = re.sub("[%s]" % re.escape("!|#|$|%|&|'|(|)|*|+|,|-|.|:|;|<|=|>|?|@|[|]|^|_|`|{|}|~"), "", parsed)
    # add a underscore between fluid and ounces
    parsed = re.sub(r"((fluid)\s(ounces))", "fluid_ounces", parsed)
    # token words in the ingredients
    tokenized = word_tokenize(parsed)
    # instantiate Lemmatizer from NLTK to lemmatize text (return them to root words)
    wnl = WordNetLemmatizer()
    # lemmatize the words and place in new list
    lemmatized = [wnl.lemmatize(token.lower()) for token in tokenized]
    # remove punctuation again per word
    parsed_tokens = [re.sub("[%s]" % re.escape("!|#|$|%|&|'|(|)|*|+|,|-|.|:|;|<|=|>|?|@|[|]|^|_|`|{|}|~"), "", root) for root in lemmatized]
    # loop through tokens and return it if it is in the list of defined units
    for parsed_token in parsed_tokens:
        try:
            if parsed_token in units:
                return parsed_token
        except:
                return None

# create function to parse out ingredients
def get_ingredients(ingredient):
    
    # lower case words
    lowered = ingredient.lower()
    # remove all text between parentheses ingredients
    parsed = re.sub(r"([(][^(]+[$)])", "", lowered)
    # remove all numbers
    parsed = re.sub(r"(\d?)", "", parsed)
    # split ingredients into a list
    parsed = parsed.split(", ")
    # remove punctuation
    parsed = [re.sub("[%s]" % re.escape(string.punctuation), "", p) for p in parsed]
    # strip whitespace
    parsed = [p.strip(" ") for p in parsed]
    # instantiate lemmatizer from NLTK
    wnl = WordNetLemmatizer()
    # lemmatize the words and place in new list
    lemmatized = [wnl.lemmatize(p) for p in parsed]
    # tokenize each item
    tokenized_list = [word_tokenize(lemma) for lemma in lemmatized]
    # remove stop words
    tokens = []
    for words_list in tokenized_list:
        words = []
        for word in words_list:
            if word not in stop_words and word != [] and word not in ["salt", "black pepper", "yellow"]:
                words.append(word)
        tokens.append("_".join(words))
        return " ".join(tokens)



