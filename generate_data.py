"""
Tai bo du lieu Wine Quality (UCI) va chia thanh ba file:
  data/train_phase1.csv  (2998 mau) - huan luyen ngay bay gio
  data/eval.csv           (500 mau)  - held-out set, khong bao gio dung de train
  data/train_phase2.csv  (2998 mau) - du lieu bo sung cho muc 4.8

Nguon: https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/
"""

import os
import numpy as np
import pandas as pd

RED_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
WHITE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv"

FEATURE_RENAME = {
    "fixed acidity": "fixed_acidity",
    "volatile acidity": "volatile_acidity",
    "citric acid": "citric_acid",
    "residual sugar": "residual_sugar",
    "chlorides": "chlorides",
    "free sulfur dioxide": "free_sulfur_dioxide",
    "total sulfur dioxide": "total_sulfur_dioxide",
    "density": "density",
    "pH": "pH",
    "sulphates": "sulphates",
    "alcohol": "alcohol",
}

FEATURE_ORDER = [
    "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
    "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
    "pH", "sulphates", "alcohol", "wine_type",
]

N_TRAIN_PHASE1 = 2998
N_EVAL = 500
N_TRAIN_PHASE2 = 2998

RANDOM_STATE = 42


def quality_to_target(quality: int) -> int:
    if quality <= 5:
        return 0  # thap
    if quality == 6:
        return 1  # trung_binh
    return 2  # cao


def load_and_prepare() -> pd.DataFrame:
    red = pd.read_csv(RED_URL, sep=";")
    white = pd.read_csv(WHITE_URL, sep=";")

    red["wine_type"] = 0
    white["wine_type"] = 1

    df = pd.concat([red, white], ignore_index=True)
    df = df.rename(columns=FEATURE_RENAME)
    df["target"] = df["quality"].astype(int).apply(quality_to_target)
    df = df[FEATURE_ORDER + ["target"]]

    df = df.sample(frac=1.0, random_state=RANDOM_STATE).reset_index(drop=True)
    return df


def main():
    os.makedirs("data", exist_ok=True)
    df = load_and_prepare()

    total_needed = N_TRAIN_PHASE1 + N_EVAL + N_TRAIN_PHASE2
    if len(df) < total_needed:
        raise SystemExit(
            f"Khong du du lieu: co {len(df)}, can {total_needed}."
        )

    train_phase1 = df.iloc[0:N_TRAIN_PHASE1]
    eval_df = df.iloc[N_TRAIN_PHASE1:N_TRAIN_PHASE1 + N_EVAL]
    train_phase2 = df.iloc[
        N_TRAIN_PHASE1 + N_EVAL:N_TRAIN_PHASE1 + N_EVAL + N_TRAIN_PHASE2
    ]

    train_phase1.to_csv("data/train_phase1.csv", index=False)
    eval_df.to_csv("data/eval.csv", index=False)
    train_phase2.to_csv("data/train_phase2.csv", index=False)

    print(f"train_phase1.csv : {len(train_phase1)} mau")
    print(f"eval.csv         : {len(eval_df)} mau")
    print(f"train_phase2.csv : {len(train_phase2)} mau")


if __name__ == "__main__":
    main()
