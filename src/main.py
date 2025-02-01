import os
from utils import (
    load_eeg_arff,
    get_sampling_rate_from_dataframe,
    visualize_eye_state_over_time,
    analyze_alpha_stability,
)


def main():
    # Duration of the measurement in seconds
    duration_of_measurement = 117

    # Relative path to the data file
    relative_path_to_data = "../data/EEG_Eye_State.arff"

    # Get the absolute path to the data file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, relative_path_to_data)

    # Load the data from the file
    df = load_eeg_arff(file_path, False)

    # Calculate the sampling rate from the dataframe and measurement duration
    sampling_rate = get_sampling_rate_from_dataframe(df, duration_of_measurement)

    # Visualize eye state over time
    visualize_eye_state_over_time(df, sampling_rate)

    # List of EEG channels for alpha stability analysis
    eeg_channels = ["O1", "O2", "P7", "P8"]

    # Analyze alpha stability for each specified EEG channel
    for channel in eeg_channels:
        analyze_alpha_stability(df, eeg_channel=channel, sampling_rate=sampling_rate)


if __name__ == "__main__":
    main()
