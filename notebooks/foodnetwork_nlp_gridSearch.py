"""
Import Packages
"""

# data wrangling tools
import pandas as pd
import re

# visualization tools
import matplotlib.pyplot as plt
import numpy as np
import pyLDAvis
import pyLDAvis.gensim
import pyLDAvis.sklearn
from pprint import pprint

# nlp tools
import spacy
import nltk
nltk.download('stopwords')
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer, PorterStemmer
import gensim
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD, NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV

# save files
import pickle

# disable warnings that bring up a deprecation warning
import warnings
warnings.filterwarnings("ignore")

"""
Helper Functions
"""

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

# create function to further clean each ingredient string
def clean_ingredients(ingredient):
    if ingredient != None:
        cleaned = ingredient.lower()
        cleaned = ingredient.replace("uncategorized", "")
        
        parsed = re.sub("(\d?)", "", cleaned)
        return parsed

# define function to pick model after it is fit
def pickle_model(model_name, model):
    model_pickle_path = './foodnetwork_{}.pkl'.format(model_name)
    model_pickle = open(model_pickle_path, 'wb')
    pickle.dump(model, model_pickle)
    model_pickle.close()

""" Import Data """

# read in pickled data for topic modeling ingredients
ingredients_grouped = pd.read_pickle("foodnetwork_ingred_grp_sklearn.pkl")

"""
Grid Search for Best Parameters with Latent Dirichlet Allocation (LDA) 
and Non-Negative Matrix Factorization (NMF) Using Scikit-Learn
"""

""" Read in model pickles """

# sklearn nmf model
tfidf_pickle = open('./foodnetwork_tfidf_sklearn.pkl', 'rb')
tfidf = pickle.load(tfidf_pickle)
# print("NMF Base Model:")
# print(tfidf)

# sklearn lda model
tf_pickle = open('./foodnetwork_tf_sklearn.pkl', 'rb')
tf = pickle.load(tf_pickle)
# print("LDA Base Model:")
# print(tf)

""" Models """

# Define Search Parameters
search_params = {'n_components': [10, 15, 20, 25, 30, 40, 50, 60, 70], 'learning_decay': [.5, .7, .9]}

# Init the Model
lda = LatentDirichletAllocation()

# Init Grid Search Class
model = GridSearchCV(lda, param_grid=search_params)

# Do the Grid Search
lda_gs = model.fit(tf)

# Best Model
best_lda_model = model.best_estimator_

# Pickle Best Model
# pickle_model("tf_sklearn_best", best_lda_model)

# # Model Parameters
# print("Best Model's Params: ", model.best_params_)

# # Log Likelihood Score
# print("Best Log Likelihood Score: ", model.best_score_)

# # Perplexity
# print("Model Perplexity: ", best_lda_model.perplexity(tf))

# print(model.cv_results_["params"])

# print(model.cv_results_["mean_test_score"])

""" Analysis of the Results"""

# Create Document - Topic Matrix
lda_output = best_lda_model.transform(tf)

# column names
topicnames = ["Topic" + str(i+1) for i in range(best_lda_model.n_components)]

# index names
docnames = ["Recipe_" + str(i+1) for i in range(len(ingredients_grouped))]

# Make the pandas dataframe
df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)

# Get dominant topic for each document
dominant_topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic['dominant_topic'] = dominant_topic

# Styling
def color_green(val):
    color = 'green' if val > .1 else 'black'
    return 'color: {col}'.format(col=color)

def make_bold(val):
    weight = 700 if val > .1 else 400
    return 'font-weight: {weight}'.format(weight=weight)

# Apply Style
df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)
# print(df_document_topics)

df_topic_distribution = df_document_topic['dominant_topic'].value_counts().reset_index(name="Num Documents")
df_topic_distribution.columns = ['Topic Num', 'Num Documents']
# print(df_topic_distribution)

# pyLDAvis.enable_notebook()
# panel = pyLDAvis.sklearn.prepare(best_lda_model, data_vectorized, vectorizer, mds='tsne')
# panel

# Topic-Keyword Matrix
df_topic_keywords = pd.DataFrame(best_lda_model.components_)

# define number of max features
no_features = 1000

# define documents to vectorize
documents = ingredients_grouped.ingredient_parsed

# Instantiate vectorizer
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

# Assign Column and Index
df_topic_keywords.columns = tf_feature_names
df_topic_keywords.index = topicnames

# Styling
def color_red(val):
    color = 'red' if val > 1 else 'black'
    return 'color: {col}'.format(col=color)

def make_bold_red(val):
    weight = 700 if val > 1 else 400
    return 'font-weight: {weight}'.format(weight=weight)

# View
df_topic_keywords = df_topic_keywords.style.applymap(color_red).applymap(make_bold_red)

# Show top n keywords for each topic
def show_topics(vectorizer, lda_model, n_words=20):
      keywords = np.array(vectorizer.get_feature_names())
      topic_keywords = []
      for topic_weights in lda_model.components_:
          top_keyword_locs = (-topic_weights).argsort()[:n_words]
          topic_keywords.append(keywords.take(top_keyword_locs))
      return topic_keywords

topic_keywords = show_topics(vectorizer=tf_vectorizer, lda_model=best_lda_model, n_words=15)        

# Topic - Keywords Dataframe
df_topic_keywords = pd.DataFrame(topic_keywords)
df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
# print(df_topic_keywords)

"""## Clustering Documents with Similar Topics and Visualization"""

# Construct the k-means clusters
from sklearn.cluster import KMeans
clusters = KMeans(n_clusters=15, random_state=100).fit_predict(lda_output)

# Build the Singular Value Decomposition(SVD) model
svd_model = TruncatedSVD(n_components=2)  # 2 components
lda_output_svd = svd_model.fit_transform(lda_output)

# X and Y axes of the plot using SVD decomposition
x = lda_output_svd[:, 0]
y = lda_output_svd[:, 1]

# # Weights for the 15 columns of lda_output, for each component
# print("Component's weights: \n", np.round(svd_model.components_, 2))

# # Percentage of total information in 'lda_output' explained by the two components
# print("Perc of Variance Explained: \n", np.round(svd_model.explained_variance_ratio_, 2))

# Plot
plt.figure(figsize=(12, 12))
plt.scatter(x, y, c=clusters)
plt.xlabel('Component 2')
plt.xlabel('Component 1')
plt.title("Segregation of Topic Clusters", )
plt.show()

