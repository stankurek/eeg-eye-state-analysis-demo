import numpy as np
import pandas as pd
from scipy.signal import hilbert
from .signal_processing import alpha_bandpass_filter
from .plotting import plot_alpha_stability, plot_alpha_band_activity, plot_eye_state


# Analyze and plot the eye state over time
def analyze_eye_state_over_time(df: pd.DataFrame, sampling_rate: int) -> None:
    time = df.index / sampling_rate
    plot_eye_state(time, df["eyeDetection"].values)


# Analyze alpha band stability over time for a specific EEG channel
def analyze_alpha_stability(
    df: pd.DataFrame, eeg_channel: str, sampling_rate: int, window_size: int = 5
) -> None:
    samples_per_window = window_size * sampling_rate
    alpha_signal = alpha_bandpass_filter(df[eeg_channel].values, fs=sampling_rate)

    avg_alpha_open = []
    avg_alpha_closed = []
    window_times = []

    for start in range(0, len(df) - samples_per_window, samples_per_window):
        end = start + samples_per_window
        window_df = df.iloc[start:end]
        window_alpha = alpha_signal[start:end]

        open_mask = window_df["eyeDetection"] == 0
        closed_mask = window_df["eyeDetection"] == 1

        mean_open = (
            np.mean(np.abs(window_alpha[open_mask]))
            if np.any(open_mask)
            else float("nan")
        )
        mean_closed = (
            np.mean(np.abs(window_alpha[closed_mask]))
            if np.any(closed_mask)
            else float("nan")
        )

        avg_alpha_open.append(mean_open)
        avg_alpha_closed.append(mean_closed)
        window_times.append(window_df.index[0] / sampling_rate)

    plot_alpha_stability(window_times, avg_alpha_open, avg_alpha_closed, eeg_channel)


# Analyze and plot frequency of the alpha band along with mean values
def analyze_alpha_band_activity_with_means(
    df: pd.DataFrame, eeg_channel: str, sampling_rate: int
) -> None:
    filtered_signal = alpha_bandpass_filter(df[eeg_channel].values, fs=sampling_rate)

    analytic_signal = hilbert(filtered_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = np.diff(instantaneous_phase) * (
        sampling_rate / (2.0 * np.pi)
    )
    time_axis = (df.index / sampling_rate)[1:]

    open_eyes_freq = []
    closed_eyes_freq = []
    eye_detection = df["eyeDetection"].iloc[1:].values

    for i, freq in enumerate(instantaneous_frequency):
        if 8 <= freq <= 13:
            if eye_detection[i] == 0:
                open_eyes_freq.append(freq)
            else:
                closed_eyes_freq.append(freq)

    mean_open = np.mean(open_eyes_freq) if open_eyes_freq else 0
    mean_closed = np.mean(closed_eyes_freq) if closed_eyes_freq else 0

    plot_alpha_band_activity(
        time_axis,
        instantaneous_frequency,
        mean_open,
        mean_closed,
        eye_detection,
        eeg_channel,
    )
