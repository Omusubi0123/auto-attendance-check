# auto-attendance-check

自動で出欠確認を行うプログラムです。

## 環境作成

Windwosではpowerhsell上で以下のコマンドを実行

```powershell
python -m venv aac_env
./aac_env/Scripts/Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

vscodeではインタープリター選択から`./aac_env/cripts/python.exe`を指定

## ローカル環境でのリントおよびテスト

```powershell
black . --exclude aac_env
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude aac_env
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude aac_env
pytest
```
