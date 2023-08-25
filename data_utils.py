import os
import pandas as pd

def read_data_from_csv(file_path):
    return pd.read_csv(file_path)

def load_data(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    data_frames = []

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        data_frame = read_data_from_csv(file_path)
        data_frames.append(data_frame)

    df = pd.concat(data_frames, ignore_index=True)

    # Ensure the desired columns exist in the DataFrame
    desired_columns = ['Keyword', 'Title', 'Subtitle', 'Summary', 'Search Term', 'Question', 'Answer', "Tags", "Sentiment Analysis", "Rating"]
    for col in desired_columns:
        if col not in df.columns:
            df[col] = None

    text_columns = ['Keyword', 'Title', 'Subtitle', 'Summary', 'Search Term', 'Question', 'Answer', "Tags"]
    df[text_columns] = df[text_columns].fillna('')
    df['combined_text'] = df[text_columns].apply(lambda x: ' '.join(x), axis=1)

    return df
