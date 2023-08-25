import spacy
import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = None
user_item_similarity = None

# Load the 'en_core_web_sm' model only if it's not present
if 'en_core_web_sm' not in spacy.util.get_installed_models():
    spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')



def initialize_recommendations(dataframe):
    global tfidf_matrix, user_item_similarity
    tfidf_matrix = tfidf_vectorizer.fit_transform(dataframe['combined_text'])
    user_item_similarity = cosine_similarity(tfidf_matrix)

def get_content_based_recommendations(dataframe, query):
    query_vector = tfidf_vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    similar_articles = cosine_similarities.argsort()[-5:][::-1]
    recommendations = dataframe.iloc[similar_articles]
    return recommendations

def get_hybrid_recommendations(dataframe, query, top_n=5):
    content_rec = get_content_based_recommendations(dataframe, query)
    if not content_rec.empty:
        idx = content_rec.index[0]
        sim_scores = list(enumerate(user_item_similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        similar_articles = [i[0] for i in sim_scores[1:top_n+1]]
        collab_rec = dataframe.iloc[similar_articles]
    else:
        collab_rec = pd.DataFrame()

    combined_recommendations = pd.concat([content_rec, collab_rec], ignore_index=True).drop_duplicates()
    combined_recommendations['Sentiment Analysis'] = combined_recommendations['combined_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    positive_rec = combined_recommendations[combined_recommendations['Sentiment Analysis'] > 0].sort_values(by='Sentiment Analysis', ascending=False)
    neutral_rec = combined_recommendations[combined_recommendations['Sentiment Analysis'] == 0]
    sorted_recommendations = pd.concat([positive_rec, neutral_rec], ignore_index=True)
    sorted_recommendations = sorted_recommendations.sort_values(by=['Sentiment Analysis', 'Rating'], ascending=[False, False], na_position='last')
    
    return sorted_recommendations[:top_n]
