# main.py

import pandas as pd

from src.data.load_data import load_data
from src.data.preprocess import prepare_datasets, transform_survival_probability
from src.models.evaluate import score
from src.models.predict import create_submission
from src.models.train import train_model


def main():
    # 데이터 경로
    train_path = "./data/raw/train.csv"
    test_path = "./data/raw/test.csv"

    # 1. 데이터 로드
    train, test = load_data(train_path, test_path)

    # 2. 생존 확률 변환
    train["y"] = transform_survival_probability(train, time_col="efs_time", event_col="efs")

    # 3. Feature 준비
    train_x, train_y, test_x, total = prepare_datasets(train, test)

    # 4. 모델 학습 및 예측
    oof_xgb, pred_xgb, model_xgb = train_model(train_x, train_y, test_x)

    # 5. 평가
    y_true = train[["ID", "efs", "efs_time", "race_group"]].copy()
    y_pred = pd.DataFrame({"ID": train["ID"], "prediction": oof_xgb})
    c_index = score(y_true, y_pred, "ID")
    print(f"\nOverall CV for XGBoost KaplanMeier: {c_index:.4f}")

    # 6. 제출 파일 생성
    create_submission(test_ids=test["ID"], predictions=pred_xgb, output_path="submission.csv")


if __name__ == "__main__":
    main()
