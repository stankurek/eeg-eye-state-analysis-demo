import os
from utils import load_eeg_arff, eeg_dataframe_to_json


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../data/EEG_Eye_State.arff")

df = load_eeg_arff(file_path)
json_data = eeg_dataframe_to_json(df)
print(json_data)
