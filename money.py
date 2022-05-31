from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
from settings import *

def fetch_mochikabu():
    url = "https://mochikabukai.mizuho-sc.com/kai/KiLoginPre.do"

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    if 'システムメンテナンス中' in driver.page_source:
        print('not avairable')
        sys.exit(0)

    driver.switch_to.frame(1)
    driver.switch_to.frame
    time.sleep(2)

    mochikabu_form = driver.find_element_by_name("kiLoginInDTO.motikabuCd")
    mochikabu_form.send_keys(MOCHIKABU_CODE)
    time.sleep(1)

    kaiin_form = driver.find_element_by_name("kiLoginInDTO.compositeKaiinCd")
    kaiin_form.send_keys(MOCHIKABU_KAIIN)
    time.sleep(1)

    password_form = driver.find_element_by_name("kiLoginInDTO.password")
    password_form.send_keys(MOCHIKABU_PASS)
    time.sleep(1)

    driver.find_element_by_xpath('//input[@value="ログイン"]').click()

    ### ログイン後、パスワード変更入力画面
    driver.find_element_by_xpath('//a[@href="KiTopPre.do"]').click()

    ### 「照会」ボタンクリック
    driver.switch_to.frame(0)
    driver.find_element_by_class_name("shoukai").click()

    ### 「会員残高照会」をクリック
    driver.switch_to.parent_frame()
    driver.switch_to.frame(1)
    driver.find_element_by_xpath('//a[@href="KiZndkSyokConf.do"]').click()

    ### データ取得
    soup = BeautifulSoup(driver.page_source, "html.parser")
    infos = soup.find_all("table", attrs={"class":"tblbasic"})

    data = {
        "Ym": str(infos[0].find_all("td")[2].text.replace('\xa0給与','')),
        "kabu": float(infos[0].find_all("td")[3].text.replace('株', '')),
        "_mod": int(infos[0].find_all("td")[4].text.replace('円', '')),
        "_avg": float(infos[0].find_all("td")[5].text.replace('円', '').replace(',',''))
    }

    driver.close()

    return data

def insert_to_sheet(data):
    scope  = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds  = ServiceAccountCredentials.from_json_keyfile_name(GSPREAD_SECRET_PATH, scope)
    client = gspread.authorize(creds)

    books  = client.open_by_key(MOCHIKABU_SHEET_KEY)
    sheet  = books.worksheet(MOCHIKABU_SHEET_NAME)

    kabuka = float(sheet.acell('B1').value.replace(chr(165),'').replace(',',''))

    data_arr = [data['Ym'], data['kabu'], data['_mod'], data['_avg'], kabuka]

    if sheet.col_values(1)[-1] < data['Ym']:
        sheet.append_row(data_arr)
    else:
        sys.exit(0)


if __name__ == "__main__":
    data = fetch_mochikabu()
    print(data)
    insert_to_sheet(data)
