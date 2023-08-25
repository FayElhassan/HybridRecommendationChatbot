import os
import pandas as pd

def read_data_from_csv(file_path):
    return pd.read_csv(file_path)
import pandas as pd

def load_data_from_github():
    base_url = "https://raw.githubusercontent.com/FayElhassan/HybridRecommendationChatbot/main/Pages%20Preprocessed/"
    
    file_names = [
        "data_for_recommendation%20-%20data_for_recommendation.csv",
        "medium_data_-_Sheet1.csv",
        "preprocessed_AIClubWorld.csv",
        "preprocessed_AIGPTInsights.csv",
        "preprocessed_AIKnowledgeBase.csv",
        "preprocessed_DeepLearningAIHQ.csv",
        "preprocessed_GitHubCopilot.csv",
        "preprocessed_NVIDIAAI.csv",
        "preprocessed_machinelearningandAI.csv",
        "preprocessed_master.of.code.global.csv",
        "preprocessed_metaai.csv",
        "preprocessed_openai.csv",
        "preprocessed_openai.research.csv",
        "preprocessed_procodeai.csv",
        "preprocessed_profile.php?id=100094681485185.csv",
        "quorascrape_-_quorascrape.csv"
    ]
    
    dfs = []
    for file_name in file_names:
        url = base_url + file_name
        df = pd.read_csv(url)
        dfs.append(df)
    
    # You can concatenate the dataframes if needed
    concatenated_df = pd.concat(dfs, ignore_index=True)
    
    return concatenated_df  # or return concatenated_df if you want a single dataframe

# def load_data(folder_path):
#     csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
#     data_frames = []

#     for csv_file in csv_files:
#         file_path = os.path.join(folder_path, csv_file)
#         data_frame = read_data_from_csv(file_path)
#         data_frames.append(data_frame)

#     df = pd.concat(data_frames, ignore_index=True)

#     # Ensure the desired columns exist in the DataFrame
#     desired_columns = ['Keyword', 'Title', 'Subtitle', 'Summary', 'Search Term', 'Question', 'Answer', "Tags", "Sentiment Analysis", "Rating"]
#     for col in desired_columns:
#         if col not in df.columns:
#             df[col] = None

#     text_columns = ['Keyword', 'Title', 'Subtitle', 'Summary', 'Search Term', 'Question', 'Answer', "Tags"]
#     df[text_columns] = df[text_columns].fillna('')
#     df['combined_text'] = df[text_columns].apply(lambda x: ' '.join(x), axis=1)

#     return df
