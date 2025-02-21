import numpy as np
import pandas as pd


def create_submission(test_ids: pd.Series, predictions: np.ndarray, output_path: str):
    submission = pd.DataFrame({"ID": test_ids, "Prediction": predictions})
    submission.to_csv(output_path, index=False)
    print("\nSubmission file saved as 'submission.csv'")
