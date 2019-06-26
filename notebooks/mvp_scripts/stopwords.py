import string
from nltk.corpus import stopwords

""" Prepare Stopwords. """
# assign the base copy of stopwords from NLTK to variable
stop_words = stopwords.words("english")

# define additional stop words to include in the list
user_defined_stops = ["from", "subject", "edu", "re", "edu", "use", "tablespoon", "tbsp", "tbs", "tbl", "tablespoons", "teaspoon", "tsp", "teaspoons",
                "ounce", "ounces", "fluid ounce", "fluid ounces", "oz", "fluid oz", "fl oz", "gill", "cup", "cups", "c", "C", "pint", "pt", "fluid pint", 
                "fl pt", "quart", "qt", "fluid quart", "fl qt", "gallon", "liter", "litre", "L", "milliliter", "millilitre", "mL", "ml", "deciliter", 
                "dl", "dL", "decilitre", "gal", "gram", "gramme", "g", "pound", "pounds", "lb", "milligram", "mg", "decigram", "dg", "kilogram", "kg", "kilogramme", 
                "millimeter", "millimetre", "mm", "decimeter", "decimetre", "dm", "meter", "metre", "m", "kilometer", "kilometre", "kilo", "km", 
                "centimeter", "centimetre", "cm", "inch", "in", "cubic meter", "cm3", "m3", "mm3", "km3", "celsius", "Celsius", "Fahrenheit", "F", 
                "pinch", "handful", "loaf", "dash", "Dash", "stick", "recipe", "recipe follows", "follows", "follow", "fluid", "large", "little", "medium", "edium"
                "a", "an", "is", "of", "glug", "good" "accompaniment", "as an accompaniment", "dusting", "a good glug of", "for", "at", "room", 
                "temperature", "room temperature", "loosely", "packed", "loosely packed", "package", "bags", "bag", "thinly", "thin", "sliced", 
                "slice", "ground", "container", "ontainer", "cored", "stoned", "instant", "thickly", "thick", "plu", "inche", "box", "inches", "good", 
                "freshly", "desired", "long", "lengthwise", "halve", "halved", "love", "cracked", "sprig", "chopped", "l", "minced", "smashed", "softened", 
                "small", "turn", "pan", "greasing", "seeded", "peeled", "storebought", "finely", "dish", "ripe", "dozen", "fresh", "frozen", "packages", 
                "cookandserve", "cooked", "cook", "serve", "sharptasting", "skinon", "warmed", "microwave", "whole", "slab", "drained", "diced", "cans", "can", 
                "plus", "grated", "head", "for", "frying", "favorite", "oneandahalf", "unseasoned", "unbleached", "lukewarm", "quick", "crushed", "one", "coarse", 
                "grained", "nosaltadded", "unsalted", "dashes", "two", "inchlong", "would", "probably", "buy", "around", "garnish", "tops", "tap", "bunch", "kernel", "snipped", "envelope", "drizzle"]

# add the user defined stopwords above and punctuation to the stop words list for cleaning
stop_words.extend(user_defined_stops + list(string.punctuation))