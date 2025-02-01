import matplotlib.pyplot as plt
import numpy as np


# Plot the eye state over time
def plot_eye_state(time: np.ndarray, eye_state: np.ndarray) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(time, eye_state, label="Eye State (0=open, 1=closed)", color="black")
    plt.xlabel("Time (s)")
    plt.ylabel("Eye State")
    plt.title("Eye State Over Time")
    plt.yticks([0, 1])
    plt.legend(loc="upper right")
    plt.show()


# Plot the stability of the alpha band amplitude for eyes open and closed
def plot_alpha_stability(
    window_times, avg_alpha_open, avg_alpha_closed, channel: str
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(
        window_times,
        avg_alpha_open,
        label="Eyes Open (Alpha Amplitude)",
        color="blue",
        marker="o",
    )
    plt.plot(
        window_times,
        avg_alpha_closed,
        label="Eyes Closed (Alpha Amplitude)",
        color="red",
        marker="o",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Average Alpha Amplitude (µV)")
    plt.title(f"Alpha Band Stability (8-13 Hz) - Channel {channel}")
    plt.legend()
    plt.show()


# Plot the instantaneous frequency of the alpha band along with mean frequency lines
def plot_alpha_band_activity(
    time_axis,
    instantaneous_frequency,
    open_mean: float,
    closed_mean: float,
    eye_detection,
    channel: str,
) -> None:
    plt.figure(figsize=(12, 6))
    for i in range(len(time_axis) - 1):
        color = "blue" if eye_detection[i + 1] == 0 else "red"
        plt.plot(
            [time_axis[i], time_axis[i + 1]],
            [instantaneous_frequency[i], instantaneous_frequency[i + 1]],
            color=color,
        )

    plt.axhline(
        open_mean,
        color="blue",
        linestyle="--",
        linewidth=2,
        label=f"Mean Open Eyes: {open_mean:.2f} Hz",
    )
    plt.axhline(
        closed_mean,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Mean Closed Eyes: {closed_mean:.2f} Hz",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title(f"Alpha Band Activity (8-13 Hz) - Channel {channel}")
    plt.ylim(6, 15)
    plt.legend()
    plt.grid(True)
    plt.show()
