import os
from utils import load_eeg_arff, get_sampling_rate_from_dataframe, visualize_eye_state_over_time, analyze_alpha_stability


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../data/EEG_Eye_State.arff")

df = load_eeg_arff(file_path, False)
sampling_rate = get_sampling_rate_from_dataframe(df, 117)
visualize_eye_state_over_time(df, sampling_rate)
analyze_alpha_stability(df, eeg_channel="O1", window_size=5, sampling_rate=sampling_rate)
