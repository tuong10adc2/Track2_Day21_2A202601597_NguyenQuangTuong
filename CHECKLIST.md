# Checklist - MLOps Lab

Repo: https://github.com/tuong10adc2/Track2_Day21_2A202601597_NguyenQuangTuong

Chu thich trang thai: `[DA XONG]` `[DANG CHO XU LY]` `[CHUA LAM]`

## Phan 1 - Cong viec cua Claude

- [x] **[DA XONG]** `generate_data.py` - tu viet moi (repo ban dau rong, khong co san file nay).
      Tai that Wine Quality tu UCI (1599 do + 4898 trang), gan `wine_type`, map
      `quality -> target` (0/1/2), shuffle `random_state=42`, chia dung **2998 / 500 / 2998** mau.
- [x] **[DA XONG]** `add_new_data.py` - tu viet moi. Gop `train_phase2.csv` vao
      `train_phase1.csv`, da test cho dung ket qua **2998 -> 5996** mau, sau do phuc hoi lai
      data goc.
- [x] **[DA XONG]** `src/train.py` - dien du 10 TODO: doc data, tach X/y,
      `mlflow.start_run()`, log params/metrics (accuracy, f1_score), log model, ghi
      `outputs/metrics.json` va `models/model.pkl`, tra ve `acc`. `random_state=42` bat buoc.
- [x] **[DA XONG]** `src/serve.py` - dien du 8 TODO: `download_model()` tu GCS luc khoi dong
      module (chi 1 lan), `/health` tra `{"status": "ok"}`, `/predict` validate du 12 features
      va tra ve `{"prediction": 0|1|2, "label": "thap"|"trung_binh"|"cao"}`.
- [x] **[DA XONG]** `tests/test_train.py` - dien du 10 TODO, sinh data ngau nhien trong bo nho
      (khong dung cloud). Da chay `pytest tests/ -v` -> **3 passed**.
- [x] **[DA XONG]** `.github/workflows/mlops.yml` - dien du 8 TODO: 4 job
      `Test -> Train -> Eval -> Deploy` noi tiep bang `needs:`. Job `Eval` dung `float()`
      truoc khi so sanh voi 0.70 (tranh loi so sanh chuoi).
- [x] **[DA XONG]** `params.yaml`, `requirements.txt`, `.gitignore` - da them
      `pathspec==0.11.2` de fix loi xung dot pathspec/DVC gap tren may.
- [x] **[DA XONG]** Chay that 6 lan MLflow (`sqlite:///mlflow.db`) voi params khac nhau -> deu
      co accuracy + f1_score. Bo tot nhat da chon: **n_estimators=800, max_depth=15,
      min_samples_split=2** -> accuracy = 0.714 (vuot gate 0.70). 2 run con lai duoi 0.70
      (0.54 va 0.68) lam bang chung cho phan giai thich eval gate.
- [x] **[DA XONG]** So sanh that 2998 mau (accuracy 0.714) vs 5996 mau (accuracy 0.764) - xem
      `REPORT.md`.
- [x] **[DA XONG]** `dvc init` + `dvc add` local (sau khi fix loi pathspec) -> sinh dung 3 file
      `.dvc` con tro: `data/train_phase1.csv.dvc`, `data/eval.csv.dvc`,
      `data/train_phase2.csv.dvc`. Remote dang tro toi placeholder `gs://YOUR_BUCKET_NAME/dvc`
      - se sua lai bucket that o Buoc 1 Phan 2.
- [x] **[DA XONG]** `git commit` + `git push origin main` len repo GitHub that cua may
      (branch `main`, 3 commit tinh den hien tai).
- [x] **[DA XONG]** `REPORT.md` - bao cao bang hyperparameter, so sanh accuracy/f1 truoc-sau
      khi them data, giai thich vi sao eval gate can thiet, kho khan gap phai.
- [x] **[DA XONG]** Mo phong logic eval gate cuc bo (dung code that trong job `eval`) tren 3
      accuracy that: 0.54 -> FAILED, 0.68 -> FAILED, 0.714 -> PASSED.
- [x] **[DA XONG]** Cai gcloud CLI (ban 581.0.0) va them vao PATH vinh vien, dang nhap thanh
      cong bang `tuong10adc2@gmail.com`.
- [x] **[DA XONG]** Da tao san project rong `mlops-lab-tuong-2026` cho lab (chua co billing).

## TRANG THAI HIEN TAI: Phan cloud dang [DANG CHO XU LY]

Ly do: ca 2 billing account cua tai khoan Google (`My Billing Account`, `Firebase Payment`)
deu dang o trang thai dong (`open: false`) do the thanh toan bi khoa. Khong co billing dang
mo thi khong project nao (moi hay cu) tao duoc bucket/VM. Day la gioi han ngoai kha nang xu
ly cuc bo, can nguoi dung tu mo lai/thay the phuong thuc thanh toan truoc khi tiep tuc Buoc 1
ben duoi. Xem chi tiet o `REPORT.md` muc 4.

## Phan 2 - Viec may phai tu lam, theo dung thu tu

Khong the tu dong hoa duoc vi can tai khoan cloud that, GitHub repo that, SSH vao VM that -
tat ca deu can credential/quyen so huu cua may.

### Buoc 1 - Cloud Storage + DVC (muc 4.6) - **[DANG CHO XU LY]**
0. **[DANG CHO XU LY]** Mo lai/thay the phuong thuc thanh toan cho 1 trong 2 billing account
   tren (console.cloud.google.com/billing), hoac tao billing account moi. Sau do link billing
   account do vao project `mlops-lab-tuong-2026` da tao san
   (`gcloud billing projects link mlops-lab-tuong-2026 --billing-account=<ID>`).
1. **[CHUA LAM]** Tao bucket: `gsutil mb -p mlops-lab-tuong-2026 -l us-central1 gs://<BUCKET>`
2. **[CHUA LAM]** Tao service account, cap quyen `roles/storage.objectAdmin` **chi tren bucket
   do** (khong dung `roles/storage.admin`), tao `sa-key.json` - **tuyet doi khong commit file
   nay**.
3. **[CHUA LAM]** Sua `.dvc/config`: thay `YOUR_BUCKET_NAME` bang ten bucket that (hoac chay
   lai `dvc remote add -d myremote gs://<BUCKET>/dvc -f`).
4. **[CHUA LAM]** `dvc remote modify myremote credentialpath sa-key.json`
5. **[CHUA LAM]** `dvc push`
6. **[CHUA LAM]** Kiem chung: Cloud Storage Console phai thay du lieu duoi prefix `dvc/`.
7. **[CHUA LAM]** `git add .dvc/config && git commit -m "chore: cau hinh dvc remote that" &&
   git push`

### Buoc 2 - Tao VM va cai serving (muc 4.7) - **[CHUA LAM]**
8. **[CHUA LAM]** Tao VM (`gcloud compute instances create ...`), mo firewall port 8000.
9. **[CHUA LAM]** SSH vao VM, cai `python3-pip` + `fastapi uvicorn scikit-learn joblib
   google-cloud-storage`.
10. **[CHUA LAM]** Copy `sa-key.json` va `src/serve.py` len VM (`gcloud compute scp`).
11. **[CHUA LAM]** Tao systemd service `mlops-serve` (nho thay `<YOUR_BUCKET_NAME>` bang bucket
    that trong file service). Chua start service o buoc nay - model chua co tren cloud.
12. **[CHUA LAM]** Lay IP cong khai cua VM, luu lai (`VM_IP`).

### Buoc 3 - SSH key rieng cho deploy (muc 4.8) - **[CHUA LAM]**
13. **[CHUA LAM]** `ssh-keygen -t ed25519 -f ~/.ssh/mlops_deploy -N "" -C "github-actions-deploy"`
14. **[CHUA LAM]** Them public key vao `~/.ssh/authorized_keys` tren VM.

### Buoc 4 - Khai bao GitHub Secrets (muc 4.8) - **[CHUA LAM]**
15. **[CHUA LAM]** Vao Settings -> Secrets and variables -> Actions, tao dung 5 secrets:
    `CLOUD_CREDENTIALS` (noi dung sa-key.json), `CLOUD_BUCKET`, `VM_HOST`, `VM_USER`,
    `VM_SSH_KEY` (noi dung file private key). Khong de khoang trang thua dau/cuoi.

### Buoc 5 - Chay pipeline lan dau (muc 4.11) - **[CHUA LAM]**
16. **[CHUA LAM]** Vao tab Actions, chon lan chay gan nhat (hoac push lai/`workflow_dispatch`)
    -> xac nhan ca 4 job xanh: Test -> Train -> Eval -> Deploy.
17. **[CHUA LAM]** SSH vao VM, `sudo systemctl start mlops-serve` (lan dau tien, sau khi model
    da co tren cloud storage).
18. **[CHUA LAM]** Kiem tra: `curl http://<VM_IP>:8000/health` -> `{"status": "ok"}`
19. **[CHUA LAM]** Kiem tra: `curl -X POST http://<VM_IP>:8000/predict -d '{"features": [...]}'`
    -> nhan hop le.

### Buoc 6 - Chung minh tu dong hoa lien tuc (muc 4.12) - **[CHUA LAM]**
20. **[CHUA LAM]** `python add_new_data.py` (2998 -> 5996 mau).
21. **[CHUA LAM]** `dvc add data/train_phase1.csv`
22. **[CHUA LAM]** `git add data/train_phase1.csv.dvc && git commit -m "data: bo sung 2998
    mau du lieu moi"`
23. **[CHUA LAM]** `dvc push` (bat buoc truoc buoc 24, neu khong Actions se pull data chua
    ton tai).
24. **[CHUA LAM]** `git push origin main` - buoc nay kich hoat pipeline lan hai.
25. **[CHUA LAM]** Vao tab Actions, xac nhan ten lan chay = commit message data vua roi ->
    4 job xanh.
26. **[CHUA LAM]** `curl` lai endpoint, xac nhan model moi (huan luyen tren 5996 mau) dang
    phuc vu.

### Buoc 7 - (Khuyen khich) Chung minh eval gate hoat dong tren Actions - **[CHUA LAM]**
27. **[CHUA LAM]** Tam sua `params.yaml` -> `n_estimators: 5, max_depth: 2` (mo hinh yeu, du
    kien accuracy < 0.70), push.
28. **[CHUA LAM]** Chup man hinh job `Eval` do, job `Deploy` bi bo qua (skipped/khong chay).
29. **[CHUA LAM]** Tra lai `params.yaml` ve bo tot (`n_estimators: 800, max_depth: 15,
    min_samples_split: 2`), push lai de pipeline xanh tro lai.
    (Da co ban mo phong logic gate cuc bo o Phan 1 - buoc nay la de co anh chup that tren
    GitHub Actions.)

### Buoc 8 - Chup anh nop bai, theo dung thu tu yeu cau - **[CHUA LAM]**
30. **[CHUA LAM]** MLflow UI (`mlflow ui --backend-store-uri sqlite:///mlflow.db`) - it nhat
    3 lan chay. (Du lieu 6 run da co san trong `mlflow.db`, chi can mo UI va chup.)
31. **[CHUA LAM]** Tab Actions - 4 job xanh, ca lan chay dau va lan chay kich hoat boi data.
32. **[CHUA LAM]** Ket qua `curl /health` va `curl /predict`.
33. **[CHUA LAM]** Cloud Storage Console - du lieu duoi `dvc/`, model tai
    `models/latest/model.pkl`.
34. **[CHUA LAM]** (Khuyen khich) Anh job Eval do o Buoc 7.

## Tom tat tien do

| Phan | So muc | Da xong | Dang cho | Chua lam |
|---|---|---|---|---|
| Phan 1 (Claude) | 15 | 15 | 0 | 0 |
| Phan 2 (nguoi dung) | 35 | 0 | 1 | 34 |
