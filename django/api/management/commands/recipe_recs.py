# Django
from django.core.management.base import BaseCommand, CommandError

# system tools for input function
from argparse import ArgumentParser
import sys
import os

# data cleaning and wrangling tools
import pandas as pd
import numpy as np

# nlp tools
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from .stopwords import stop_words

# metrics
from sklearn.metrics.pairwise import cosine_similarity

# pickle
import pickle

""" Create command class to allow for external script(s) to be run."""

class Command(BaseCommand):

    help = "Generate recipe recommendations."

    def add_arguments(self, parser):
        parser.add_argument('-q', dest='query', action='store_true', help='query text')
        parser.add_argument('--query', dest='query', action='store_true', help='query text')
        return parser

    def handle(self, *args, **options):

        """ Load all resources. """

        # open pickled dictionary of vocabulary and their raw term counts of the corpus of ingredients from all the recipes
        with open("api/static/lda_vocab_counts.pkl", "rb") as dict_file:
            tf_vocab = pickle.load(dict_file)

        # load the pickled LDA model
        with open("api/static/foodnetwork_lda_sklearn.pkl", "rb") as model:
            lda = pickle.load(model)

        """ Function to run raw text through pipeline for predictions. """

        # create function that runs raw text through pipeline for predictions
        def predict_topic(text):
            
            """ Preprocess input text in order to turn it into a vector and then calculate the cosine similarity scores between it and the recipes stored. """

            # # tokenize text
            # tokens = word_tokenize(text)
            
            # # instantiate lemmatizer, lowercase words, and lemmatize them
            # wnl = WordNetLemmatizer()
            # lemmatized = [wnl.lemmatize(word.lower()) for word in tokens]
            
            # # remove stop words
            # no_stops = [word for word in lemmatized if not word in stop_words]

            """ Transform preprocessed input text into a vector and transform it using the saved LDA model to obtain the topic probability scores. """

            # instantiate the CountVectorizer to convert input text into a vector
            tf_vectorizer = CountVectorizer(max_df=0.95, min_df=1, max_features=1000, vocabulary=tf_vocab)
            # use CountVectorizer to convert the preprocessed input text into a vector
            text_vector = tf_vectorizer.transform(text)
            # transform using the saved LDA model to obtain topic probability scores
            topic_probability_scores = lda.transform(text_vector)
            # return the topic and the input text's probability scores that it belongs to a specific topic
            return topic_probability_scores

        """ Function to run the preprocessed text through the function to obtain topic probability scores of the input text and then calculate cosine similarity scores between it
        and the stored recipes to find those that are most similar. """

        # function to find the top 5 recipes that fit the best with the input text
        def similar_documents(text, top_n):
            # load in the pickled reference dataframe of all the recipes assigned to respective topics and the probabilities they fit in those topics
            recipes_topics = pd.read_pickle("api/static/recipes_topics.pkl")
            # assign the probabilities of each recipe belonging to a particular topic to a variable
            doc_topic_probs = recipes_topics.Scores
            # process input text, convert into a vector, and use the LDA model to calculate its topic probability scores
            x  = predict_topic(text)
            # calculate cosine similarity between input text vector and recipe topic probability vector
            dists = cosine_similarity(x, np.array(doc_topic_probs).reshape(-1, 10))[0]
            # obtain top 5 similar recipes based on cosine similarity scores
            doc_ids = np.argsort(dists)[:top_n]
            return list(doc_ids)


        """ Define arguments to accept query, parse it, run it through LDA model, ping DB for results, and print top 5 recommended recipes. """

        if __name__ == "__main__":

            # instantiate parser
            parser = ArgumentParser()
            # add argument to parser
            parser.add_argument("-q", "--query", dest="query")
            # define values
            values = parser.parse_args()
            
            if (values.query):
                query = values.query
            else:
                print("Error: Please enter a string to be searched.")
                exit(1)

        # preprocess query text and generate the ids of the top recipes that fit it best
        doc_ids = similar_documents(args, top_n=5)
        return doc_ids