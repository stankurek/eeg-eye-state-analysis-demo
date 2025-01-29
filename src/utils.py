from scipy.io import arff
import pandas

def load_eeg_arff(file_path, verbose=True):
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
