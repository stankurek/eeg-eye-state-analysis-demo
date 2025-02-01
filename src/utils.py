from scipy.io import arff
import pandas
import matplotlib.pyplot as pyplot
from scipy.signal import butter, filtfilt, hilbert
import numpy


def load_eeg_arff(file_path, verbose=True):
    """
    Loads EEG data in arff format.
    Returns DataFrame or None.
    """
    try:
        data, metadata = arff.loadarff(file_path)
        df = pandas.DataFrame(data)

        if df.empty:
            print("The file is empty or contains no data")
            return None

        df["eyeDetection"] = df["eyeDetection"].str.decode("utf-8").astype(int)

        if verbose:
            print("EEG data:")
            print(df.head())

        return df
    except Exception as e:
        print(f"An error occurred during loading data: {e}")
        return None


def get_sampling_rate_from_dataframe(df, duration_in_seconds):
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or None.")

        samples = len(df)
        sampling_rate = samples / duration_in_seconds

        return round(sampling_rate)
    except Exception as e:
        print(f"An error occurred while calculating sampling rate: {e}")
        return None


def analyze_eye_state_over_time(df, sampling_rate):
    df["Time (s)"] = df.index / sampling_rate
    pyplot.figure(figsize=(12, 6))
    pyplot.plot(
        df["Time (s)"],
        df["eyeDetection"],
        label="Eye State (0=open, 1=closed)",
        color="black",
    )
    pyplot.xlabel("Time (seconds)")
    pyplot.ylabel("Eye State")
    pyplot.title("Eye State Over Time")
    pyplot.yticks([0, 1, 1.2], ["Open", "Closed", ""])
    pyplot.legend(loc="upper right")
    pyplot.show()


def alpha_bandpass_filter(data, fs=128):
    """
    Filters the input signal to retain only alpha waves (8-13 Hz).
    """

    # Alpha parameters
    lowcut = 8
    highcut = 13
    order = 4

    # Nyquist frequency is required for normalization of cutoff frequencies.
    nyquist = 0.5 * fs

    # Normalize the low cutoff frequency
    low = lowcut / nyquist

    # Normalize the high cutoff frequency
    high = highcut / nyquist

    # Filter only specific frequencies
    b, a = butter(order, [low, high], btype="band")

    return filtfilt(b, a, data)


def analyze_alpha_stability(df, eeg_channel="O1", sampling_rate=128):
    window_size = 5
    samples_per_window = window_size * sampling_rate

    df["Time (s)"] = df.index / sampling_rate

    alpha_signal = alpha_bandpass_filter(df[eeg_channel].values, fs=sampling_rate)

    avg_alpha_open = []
    avg_alpha_closed = []
    window_times = []

    for start in range(0, len(df) - samples_per_window, samples_per_window):
        end = start + samples_per_window
        window_data = df.iloc[start:end]
        window_alpha = alpha_signal[start:end]

        mean_open = numpy.mean(
            numpy.abs(window_alpha[window_data["eyeDetection"] == 0])
        )
        mean_closed = numpy.mean(
            numpy.abs(window_alpha[window_data["eyeDetection"] == 1])
        )

        avg_alpha_open.append(mean_open)
        avg_alpha_closed.append(mean_closed)
        window_times.append(window_data["Time (s)"].values[0])

    pyplot.figure(figsize=(10, 6))
    pyplot.plot(
        window_times,
        avg_alpha_open,
        label="Eyes Open (Alpha Amplitude)",
        color="blue",
        marker="o",
    )
    pyplot.plot(
        window_times,
        avg_alpha_closed,
        label="Eyes Closed (Alpha Amplitude)",
        color="red",
        marker="o",
    )
    pyplot.xlabel("Time (seconds)")
    pyplot.ylabel("Average Alpha Amplitude (µV)")
    pyplot.title(f"Stability of Alpha Band (8-13 Hz) - Channel {eeg_channel}")
    pyplot.legend()
    pyplot.show()


def analyze_alpha_band_activity_with_means(df, eeg_channel="O1", sampling_rate=128):
    df["Time (s)"] = df.index / sampling_rate

    filtered_signal = alpha_bandpass_filter(df[eeg_channel].values, fs=sampling_rate)

    analytic_signal = hilbert(filtered_signal)
    instantaneous_phase = numpy.unwrap(numpy.angle(analytic_signal))
    instantaneous_frequency = numpy.diff(instantaneous_phase) * (
        sampling_rate / (2.0 * numpy.pi)
    )

    time_axis = df["Time (s)"].iloc[1:].values

    open_eyes_freq = []
    closed_eyes_freq = []

    pyplot.figure(figsize=(12, 6))

    for i in range(len(time_axis) - 1):
        if 8 <= instantaneous_frequency[i] <= 13:
            color = "blue" if df["eyeDetection"].iloc[i + 1] == 0 else "red"
            pyplot.plot(
                [time_axis[i], time_axis[i + 1]],
                [instantaneous_frequency[i], instantaneous_frequency[i + 1]],
                color=color,
            )

            if df["eyeDetection"].iloc[i + 1] == 0:
                open_eyes_freq.append(instantaneous_frequency[i])
            else:
                closed_eyes_freq.append(instantaneous_frequency[i])

    mean_open_eyes = numpy.mean(open_eyes_freq) if open_eyes_freq else 0
    mean_closed_eyes = numpy.mean(closed_eyes_freq) if closed_eyes_freq else 0

    pyplot.axhline(
        mean_open_eyes,
        color="blue",
        linestyle="--",
        linewidth=2,
        label=f"Mean Open Eyes: {mean_open_eyes:.2f} Hz",
    )
    pyplot.axhline(
        mean_closed_eyes,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean Closed Eyes: {mean_closed_eyes:.2f} Hz",
    )

    pyplot.xlabel("Time (seconds)")
    pyplot.ylabel("Frequency (Hz)")
    pyplot.title(f"Alpha Band Activity (8-13 Hz) with Means - Channel {eeg_channel}")
    pyplot.ylim(6, 15)
    pyplot.legend()
    pyplot.grid(True)
    pyplot.show()
