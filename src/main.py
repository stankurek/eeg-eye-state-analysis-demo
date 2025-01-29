import os
from utils import load_eeg_arff, get_sampling_rate_from_dataframe


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../data/EEG_Eye_State.arff")

df = load_eeg_arff(file_path, False)
sampling_rate = get_sampling_rate_from_dataframe(df, 117)
print(sampling_rate)
