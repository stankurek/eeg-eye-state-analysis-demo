import logging
from pathlib import Path
from eeg_analysis.data_loader import load_eeg_arff
from eeg_analysis.signal_processing import get_sampling_rate_from_dataframe
from eeg_analysis.analysis import (
    analyze_eye_state_over_time,
    analyze_alpha_stability,
    analyze_alpha_band_activity_with_means,
)


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Measurement duration in seconds
    duration_of_measurement = 117

    # Define the path to the data file
    data_file = Path(__file__).parent / "data" / "EEG_Eye_State.arff"

    # Load the EEG data
    df = load_eeg_arff(data_file, verbose=True)
    if df is None:
        return

    # Calculate the sampling rate
    try:
        sampling_rate = get_sampling_rate_from_dataframe(df, duration_of_measurement)
    except Exception as e:
        logging.error("Failed to calculate sampling rate: %s", e)
        return

    # Analyze and plot the eye state over time
    analyze_eye_state_over_time(df, sampling_rate)

    # List of EEG channels to analyze
    eeg_channels = ["O1", "O2", "P7", "P8"]
    for channel in eeg_channels:
        analyze_alpha_stability(df, eeg_channel=channel, sampling_rate=sampling_rate)
        analyze_alpha_band_activity_with_means(
            df, eeg_channel=channel, sampling_rate=sampling_rate
        )


if __name__ == "__main__":
    main()
