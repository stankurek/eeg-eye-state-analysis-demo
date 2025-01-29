import os
from utils import load_eeg_arff, eeg_dataframe_to_json, get_sampling_rate_from_json


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../data/EEG_Eye_State.arff")

df = load_eeg_arff(file_path, False)
json_data = eeg_dataframe_to_json(df)
sampling_rate = get_sampling_rate_from_json(json_data, 117)
print(sampling_rate)
