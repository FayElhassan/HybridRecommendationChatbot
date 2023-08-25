import streamlit as st
from data_handling import load_data
from recommendation_engine import initialize_tfidf_matrix, get_hybrid_recommendations
from chat_interface import chat_interface
from sklearn.metrics.pairwise import cosine_similarity

# Load and preprocess the data
df = load_data()

# Ensure desired columns are present and handle NaN values
if not df.empty:
    desired_columns = ['Keyword', 'Title', 'Subtitle', 'Summary', 'Search Term', 'Question', 'Answer', "Tags", "Sentiment Analysis", "Rating"]
    for col in desired_columns:
        if col not in df.columns:
            df[col] = None

    text_columns = ['Keyword', 'Title', 'Subtitle', 'Summary', 'Search Term', 'Question', 'Answer', "Tags"]
    df[text_columns] = df[text_columns].fillna('')
    df['combined_text'] = df[text_columns].apply(lambda x: ' '.join(x), axis=1)

# Initialize the TF-IDF matrix and compute user-item similarity
tfidf_matrix = initialize_tfidf_matrix(df)
user_item_similarity = cosine_similarity(tfidf_matrix)

# Entry point of the application
if __name__ == "__main__":
    chat_interface(df, user_item_similarity, tfidf_matrix)
