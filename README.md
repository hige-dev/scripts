# 環境

- Ubuntu 20.04(wsl2, gce)
- Python 3.8.10

# 手順

## 1. pipをインストール

```
sudo apt update -y
sudo apt install -y python3-pip
```

## 2. 必要なパッケージをインストール

```
pip install selenium bs4 oauth2client gspread
```

### 3. chromeインストール、起動

```
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sudo apt update -y
sudo apt-get install google-chrome-stable

# background起動
google-chrome&
```

### 4. chromedriverインストール

```
google-chrome --version

# ↑と同じメジャーバージョンのchromedriverをインストールする([url](https://chromedriver.chromium.org/downloads))
cd /tmp
wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin
```

### 5. google apiの有効化

参考: https://www.twilio.com/blog/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python-jp

### 6. データを入れるシートの用意

- E2: 株価取得関数([参考](https://auto-worker.com/blog/?p=3876))
- A:E列: スクリプトで自動入力(Eはスクリプト実行時の株価なので、実際に買い付けした日付とずれがある)
- F(投資額): 持分株数(合計) * 平均買付価格 + 繰越持分現金
- G(評価額): 取得時株価 * 持分株数(合計)
- H(損益): G-F

### 7. settings.pyにパスワードなどを設定する

- MOCHIKABU_CODE  = ''
- MOCHIKABU_KAIIN = ''
- MOCHIKABU_PASS  = ''
- GSPREAD_SECRET_PATH = '5で取得したsecret.jsonのpath'
- MOCHIKABU_SHEET_KEY = 'https://docs.google.com/spreadsheets/d/{ここを抜き出す}/edit#...'
- MOCHIKABU_SHEET_NAME = 'スプレッドシートのシート名'
