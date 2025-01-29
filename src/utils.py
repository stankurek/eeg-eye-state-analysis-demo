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

def eeg_dataframe_to_json(df):
    """
    Converts EEG data to JSON.
    Returnsstring or None.
    """
    try:
        if df is None or df.empty:
            print("No data to converts")
            return None

        eeg_json = df.to_json(orient="records", indent=4)

        return eeg_json
    except Exception as e:
        print(f"An error occured during converting to JSON: {e}")
        return None
  