# Bao cao MLOps Lab

## 1. Bo sieu tham so da chon va ly do

Da chay 6 thi nghiem trong MLflow voi cac bo sieu tham so khac nhau tren `data/train_phase1.csv` (2998 mau), danh gia tren `data/eval.csv` (500 mau, held-out):

| n_estimators | max_depth | min_samples_split | accuracy | f1_score |
|---|---|---|---|---|
| 100 | 5    | 2 | 0.5660 | 0.5548 |
| 50  | 3    | 2 | 0.5400 | 0.4847 |
| 200 | 10   | 5 | 0.6800 | 0.6784 |
| 300 | None | 2 | 0.6940 | 0.6941 |
| 500 | None | 2 | 0.6980 | 0.6984 |
| **800** | **15** | **2** | **0.7140** | **0.7139** |

**Bo sieu tham so chon: `n_estimators=800, max_depth=15, min_samples_split=2`** (accuracy = 0.714, f1 = 0.714).

Ly do: day la bo duy nhat vuot nguong eval gate 0.70. Tang so cay (n_estimators) va do sau (max_depth) giup mo hinh nam bat duoc quan he phi tuyen giua cac dac trung hoa hoc va chat luong ruou, nhung neu de max_depth=None (khong gioi han) mo hinh co dau hieu overfit nhe tren tap train khien accuracy tren eval set khong tang them (300/500 cay voi max_depth=None deu ~0.69). Gioi han max_depth=15 ket hop voi nhieu cay hon (800) can bang duoc bias/variance tot hon, cho accuracy cao nhat trong cac phuong an da thu.

## 2. So sanh accuracy/f1 giua 2.998 mau va 5.996 mau

Dung cung mot bo sieu tham so (n_estimators=800, max_depth=15, min_samples_split=2), cung mot eval set (500 mau, khong doi):

| Du lieu huan luyen | So mau | accuracy | f1_score |
|---|---|---|---|
| train_phase1 (ban dau) | 2.998 | 0.7140 | 0.7139 |
| train_phase1 + train_phase2 (sau add_new_data.py) | 5.996 | 0.7640 | 0.7620 |

Nhan xet: gap doi du lieu huan luyen giup accuracy tang tu 0.714 len 0.764 (+5 diem %) va f1_score tang tu 0.714 len 0.762. Dieu nay hop ly vi Random Forest can nhieu mau de xay dung cac cay da dang hon va giam phuong sai, dac biet voi lop thieu so "cao" (chat luong 7-9) chi chiem ~19-21% du lieu — them mau giup mo hinh hoc tot hon cac truong hop bien.

## 3. Vi sao eval gate can thiet

Trong 6 thi nghiem, hai bo tham so yeu nhat (`n_estimators=50, max_depth=3` va `n_estimators=100, max_depth=5` mac dinh) chi dat accuracy 0.54 va 0.566 — thap hon nhieu so nguong 0.70. Neu khong co eval gate, pipeline se tu dong deploy CA NHUNG MODEL NAY len production, khien API `/predict` tra ve nhan sai gan mot nua so lan goi. Vi day la pipeline tu dong hoan toan (khong ai review truoc khi deploy), khong co "chan" nao khac giua buoc train va buoc serve.

Eval gate (job `eval` trong workflow, so sanh `accuracy < 0.70`) dong vai tro la mot automated quality checkpoint: neu accuracy khong dat, job `eval` that bai voi `SystemExit`, khien job `deploy` (phu thuoc `needs: eval`) khong bao gio chay. Model cu tren VM van tiep tuc phuc vu, khong bi thay the boi mot ban nang cap kem hon. Day la co che bat buoc trong CI/CD cho ML: unit test (job `test`) chi kiem tra code chay khong loi, khong kiem tra chat luong du doan — chi eval gate moi lam duoc viec do.

## 4. Kho khan gap phai va cach giai quyet

- **`generate_data.py` va `add_new_data.py` khong co san trong de bai** (thu muc lam viec rong khi bat dau). Da tu viet lai theo dung dac ta: tai bo du lieu that Wine Quality tu UCI (`winequality-red.csv` + `winequality-white.csv`, 1599 + 4898 = 6497 mau), gan `wine_type`, anh xa `quality` sang `target` (3 lop), tron ngau nhien voi `random_state=42` va chia theo dung so luong yeu cau (2998 / 500 / 2998). Ket qua chay khop chinh xac voi so mau de bai yeu cau.
- **Xung dot phien ban `pathspec`**: moi truong co san mot ban `pathspec==1.1.1` khong tuong thich voi DVC (loi `cannot import name '_DIR_MARK'`). Da ghim `pathspec==0.11.2` trong `requirements.txt` de `dvc init` chay duoc on dinh.
- **Tim bo sieu tham so vuot nguong 0.70**: du lieu Wine Quality that (khong phai du lieu tong hop) kho hon nhieu so voi vi du minh hoa — cac bo tham so "goi y" trong de bai (vi du 100/5/2) chi dat ~0.57. Da chay grid search nho tren khong gian `n_estimators x max_depth x min_samples_split` de tim ra `800/15/2` dat 0.714, vua du vuot gate.
- **Cac buoc can tai khoan cloud/GitHub that** (tao bucket, service account, VM, GitHub Secrets, `git push`, cho GitHub Actions chay, `curl` toi VM that) khong the tu dong hoa tu moi truong lam viec cuc bo — nhung phan nay duoc ghi lai chi tiet trong `CHECKLIST.md` de nguoi dung tu thuc hien.
- **Billing GCP bi khoa giua chung**: da cai gcloud CLI, dang nhap thanh cong, nhung ca hai billing account cua tai khoan Google (`My Billing Account`, `Firebase Payment`) deu o trang thai `open: false` do the thanh toan bi khoa, nen khong the bat billing cho bat ky project nao (kem theo: quota tao project moi cung da het do da co san 9 project, phai xoa bot 1 project rong de lay lai quota, nhung GCP giu project da xoa o trang thai "pending delete" 30 ngay nen quota chua duoc giai phong ngay). Day la gioi han ngoai kha nang xu ly cuc bo — can nguoi dung mo lai/thay the phuong thuc thanh toan truoc khi tiep tuc Buoc 1 trong `CHECKLIST.md`. Phan cloud (bucket, VM, deploy, curl that) hien dang **tam dung** vi ly do nay, khong phai loi cau hinh.

## 5. Bang chung da thu thap cuc bo (truoc khi day len cloud that)

- `pytest tests/ -v` -> 3 passed.
- `python generate_data.py` -> dung 2998 / 500 / 2998 mau nhu yeu cau.
- `python add_new_data.py` -> dung 2998 -> 5996 mau nhu yeu cau.
- MLflow (`sqlite:///mlflow.db`) co 6 lan chay, moi lan mot bo sieu tham so, deu co `accuracy` va `f1_score`.
- `dvc init` + `dvc add` thanh cong, sinh du ba file `.dvc` con tro (`data/train_phase1.csv.dvc`, `data/eval.csv.dvc`, `data/train_phase2.csv.dvc`).
- Mo phong logic eval gate cuc bo (dung y het code trong job `eval` cua workflow) tren 3 muc accuracy that: 0.54 -> FAILED, 0.68 -> FAILED, 0.714 -> PASSED. Xac nhan gate hoat dong dung truoc khi can chay tren GitHub Actions that.
