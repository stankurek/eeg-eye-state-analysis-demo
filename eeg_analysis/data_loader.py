from pathlib import Path
import pandas as pd
from scipy.io import arff
import logging

# Configure a logger for this module
logger = logging.getLogger(__name__)


# Load EEG data from an ARFF file
def load_eeg_arff(file_path: Path, verbose: bool = True) -> pd.DataFrame:
    try:
        data, metadata = arff.loadarff(str(file_path))
        df = pd.DataFrame(data)

        if df.empty:
            logger.error("The file is empty or contains no data.")
            return None

        df["eyeDetection"] = df["eyeDetection"].str.decode("utf-8").astype(int)
        if verbose:
            logger.info("EEG data (first 5 rows):\n%s", df.head())
        return df
    except Exception as e:
        logger.exception("Error loading data: %s", e)
        return None
