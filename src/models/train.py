import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from xgboost import XGBRegressor


def train_model(train_x: pd.DataFrame, train_y: pd.Series, test_x: pd.DataFrame, folds: int = 10):
    kf = KFold(n_splits=folds, shuffle=True, random_state=42)
    oof_xgb = np.zeros(len(train_x))
    pred_xgb = np.zeros(len(test_x))

    for i, (train_index, valid_index) in enumerate(kf.split(train_x)):
        print("#" * 25)
        print(f"### Fold {i+1}")
        print("#" * 25)

        x_train = train_x.loc[train_index].copy()
        y_train = train_y.loc[train_index].copy()
        x_valid = train_x.loc[valid_index].copy()
        y_valid = train_y.loc[valid_index].copy()
        x_test = test_x.copy()

        model_xgb = XGBRegressor(
            device="cpu",
            max_depth=3,
            colsample_bytree=0.5,
            subsample=0.8,
            n_estimators=2000,
            learning_rate=0.02,
            enable_categorical=True,
            min_child_weight=80,
            # early_stopping_rounds=25,
        )
        model_xgb.fit(x_train, y_train, eval_set=[(x_valid, y_valid)], verbose=500)

        oof_xgb[valid_index] = model_xgb.predict(x_valid)
        pred_xgb += model_xgb.predict(x_test)

    pred_xgb /= folds
    return oof_xgb, pred_xgb, model_xgb
