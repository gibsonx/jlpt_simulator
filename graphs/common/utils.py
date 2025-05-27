import pandas as pd
import json
def collect_vocabulary(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    # Shuffle the rows and reset the index
    words = data.iloc[:, :2].sample(frac=1).reset_index(drop=True)
    # Extract the second column (values) and convert to a single-line string
    vocab_string = ','.join(words.iloc[:, 1].astype(str).tolist())
    return vocab_string