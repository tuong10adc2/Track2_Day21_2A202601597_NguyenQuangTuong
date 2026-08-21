"""
Mo phong viec thu thap them du lieu: noi train_phase2.csv vao train_phase1.csv.

Truoc: data/train_phase1.csv co 2998 mau
Sau:   data/train_phase1.csv co 5996 mau (2998 + 2998)

data/train_phase2.csv khong bi thay doi, co the chay lai script nay
nhieu lan de kiem tra (moi lan se nhan doi lai tu dau vi doc ca hai file
va ghi de, khong cong don).
"""

import pandas as pd


def main():
    train_phase1 = pd.read_csv("data/train_phase1.csv")
    train_phase2 = pd.read_csv("data/train_phase2.csv")

    before = len(train_phase1)

    combined = pd.concat([train_phase1, train_phase2], ignore_index=True)
    combined.to_csv("data/train_phase1.csv", index=False)

    after = len(combined)
    print(f"Cap nhat du lieu: {before} -> {after} mau")


if __name__ == "__main__":
    main()
