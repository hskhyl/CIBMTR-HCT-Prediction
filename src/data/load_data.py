import pandas as pd


def load_data(train_path: str, test_path: str):
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.max_rows", 500)

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    print(f"Train shape: {train.shape}")
    print(f"Test shape: {test.shape}")

    return train, test
