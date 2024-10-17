import os
import random
import time
import shutil
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matlab.engine

# Google Sheets APIの設定
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.comauth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:/prog/Github_test/marine-cycle-438819-e2-05ef3300de74.json", scope
)
client = gspread.authorize(creds)

# スプレッドシートを開く
sheet = client.open_by_key("1BmLmVuvrnjFqBz4zoJ7aSgbynS0HJqPJxHLa4dZbsPg").worksheet(
    "Sheet1"
)


def check_conditions():
    # フォルダの確認
    results_dir = r"C:\prog\Github_test\Results"
    non_results_folders = [
        f
        for f in os.listdir(results_dir)
        if os.path.isdir(os.path.join(results_dir, f)) and not f.startswith("results_")
    ]

    # スプレッドシートの確認
    b2_value = sheet.acell("B2").value
    b3_value = sheet.acell("B3").value

    return len(non_results_folders) > 0 and b2_value == "" and b3_value == ""


def process_folder():
    results_dir = r"C:\prog\Github_test\Results"
    non_results_folders = [
        f
        for f in os.listdir(results_dir)
        if os.path.isdir(os.path.join(results_dir, f)) and not f.startswith("results_")
    ]

    if non_results_folders:
        folder = non_results_folders[0]
        readme_path = os.path.join(results_dir, folder, "Readme.txt")

        with open(readme_path, "r") as file:
            content = file.read()

        # 正規表現を使用して値を抽出
        send_path = re.search(r'Send Path = "(.*?)"', content).group(1)
        target_file = re.search(r'Target File = "(.*?)"', content).group(1)
        results_path = re.search(r'Results Path = "(.*?)"', content).group(1)

        # ファイルの移動
        source = os.path.join(send_path, target_file)
        destination = r"C:\prog\kawa_matlab"
        shutil.copy2(source, destination)

        # MATLABエンジンの起動と実行
        eng = matlab.engine.start_matlab()
        eng.cd(r"C:\prog\kawa_matlab")
        eng.run(target_file, nargout=0)
        eng.quit()


def main():
    while True:
        if check_conditions():
            process_folder()

        # 10〜20秒のランダムな待ち時間
        wait_time = random.uniform(10, 20)
        time.sleep(wait_time)


if __name__ == "__main__":
    main()
