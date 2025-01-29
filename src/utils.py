from scipy.io import arff
import pandas

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
  
    df['eyeDetection'] = df['eyeDetection'].str.decode('utf-8').astype(int)

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