import pandas as pd
import json
def collect_vocabulary(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    words = data.iloc[:, :2].sample(frac=1).reset_index(drop=True)
    # Display the content of the CSV file
    vocab_dict = words.set_index(words.columns[0])[words.columns[1]].to_dict()
    vocab_dict = json.dumps(vocab_dict, ensure_ascii=False, separators=(',', ':'))
    return vocab_dict