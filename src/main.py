import os
from utils import load_eeg_arff


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../data/EEG_Eye_State.arff")

df = load_eeg_arff(file_path)
print(df)

