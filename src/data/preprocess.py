import pandas as pd
from lifelines import KaplanMeierFitter


def transform_survival_probability(df, time_col="efs_time", event_col="efs"):
    kmf = KaplanMeierFitter()
    kmf.fit(df[time_col], df[event_col])
    target = kmf.survival_function_at_times(df[time_col]).values
    return target


def prepare_datasets(train, test):
    """데이터셋 준비 및 형변환"""

    # 예측대상인 y열 분리
    train_y = train["y"]

    # 훈련데이터로 쓸 칼럼 다듬기
    train_x = train.drop(["ID", "efs", "efs_time", "y"], axis=1)

    # test 데이터셋에도 ID 칼럼 제외시켜주기
    test_x = test.drop(["ID"], axis=1)

    # test 데이터와 합쳐주기
    total = pd.concat([train_x, test_x], axis=0, ignore_index=True)

    # 문자열 데이터가 곧 범주형 데이터인지 확인
    for column in total.columns:
        if total[column].dtype == "object":
            # 고유한 값의 개수를 확인하여 범주형 데이터인지 텍스트 데이터인지 판단
            unique_values = total[column].nunique()

            # 고유한 값이 50개 이하인 경우 범주형 데이터로 간주 (임의 판단)
            if unique_values <= 50:
                print(f"'{column}'은 범주형 데이터입니다. 고유 값 개수: {unique_values}")
            else:
                print(f"'{column}'은 텍스트 데이터입니다. 고유 값 개수: {unique_values}")

    # 전체 칼럼 루프 돌면서
    for column in total.columns:
        # 범주형 변수 > 결측치 메꿔주고 > 수치형으로 바꿔주기 (XGBoost가 결측치는 메꿔주는데 수치형으로는 들어가야함)
        if total[column].dtype == "object":
            total[column] = total[column].fillna("NaN")
            total[column], uniques = total[column].factorize()  # 정수형으로 변환
            total[column] -= total[column].min()  # 최솟값 빼줘서 출발점을 0으로 맞춤 일종의 정규화
            total[column] = total[column].astype("int32")  # int32로 변환하여 메모리 사용량 아껴주고
            total[column] = total[column].astype("category")  # 범주형 데이터로 바꿔서 순서, 빈도 등의 특성 유지

        # 수치형 변수 > 데이터 형변환하여 계산비용 줄여주기
        else:
            if total[column].dtype == "float64":
                total[column] = total[column].astype("float32")

            if total[column].dtype == "int64":
                total[column] = total[column].astype("int32")

    train_x = total.iloc[: len(train)].copy()

    test_x = total.iloc[len(train) :].reset_index(drop=True).copy()

    return train_x, train_y, test_x, total
