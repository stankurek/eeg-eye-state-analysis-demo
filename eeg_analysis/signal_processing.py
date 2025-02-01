import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt


# Calculate the sampling rate based on the number of samples and measurement duration
def get_sampling_rate_from_dataframe(df: pd.DataFrame, duration_in_seconds: int) -> int:
    if df is None or df.empty:
        raise ValueError("DataFrame is empty or None.")
    samples = len(df)
    sampling_rate = samples / duration_in_seconds

    return round(sampling_rate)


# Apply a bandpass filter to isolate alpha waves (8-13 Hz) from the signal
def alpha_bandpass_filter(
    data: np.ndarray,
    fs: int = 128,
    lowcut: int = 8,
    highcut: int = 13,
    order: int = 4,
) -> np.ndarray:
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")

    return filtfilt(b, a, data)
