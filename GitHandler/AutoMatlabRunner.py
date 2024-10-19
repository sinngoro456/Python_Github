import os
import time
import random
import shutil
import subprocess
import git
import MatDevider
import socket

# 定数の定義
REPO_PATH = r"C:\prog\Github_test"
MATLAB_WORK_DIR = r"C:\prog\kawa_matlab"

# 文字列定数
MATLAB_PROCESS_NAME = "MATLAB.exe"
README_FILENAME = "Readme.txt"
SEND_PATH_KEY = 'Send Path = "'
TARGET_FILE_KEY = 'Target File = "'
RESULTS_PATH_KEY = 'Results Path = "'
COMMIT_MESSAGE = "Task completed and results added"

# PCの名前を取得
pc_name = socket.gethostname()

# 定数の定義
pc_path = os.path.join(REPO_PATH, pc_name)
TASKS_PATH = os.path.join(REPO_PATH, f"{pc_name}\\tasks")  # PC名を含めたパス
RESULTS_PATH = os.path.join(REPO_PATH, f"{pc_name}\\results")  # PC名を含めたパス

# フォルダが存在しない場合は作成
os.makedirs(pc_path, exist_ok=True)
os.makedirs(TASKS_PATH, exist_ok=True)
os.makedirs(RESULTS_PATH, exist_ok=True)


def random_wait():
    # 10〜20秒のランダムな待ち時間を設定
    print("待機中...")
    time.sleep(random.uniform(1, 2))


def check_matlab_process():
    # MATLABプロセスの確認
    print("check_matlab_process")
    result = subprocess.check_output("tasklist", shell=True)
    return "MATLAB" in result.decode("utf-16")  # エンコーディングを修正


def pull_repository(repo_path):
    print("pull_repository")
    print("pull_repository")
    # リポジトリをプル
    os.chdir(repo_path)
    repo = git.Repo()
    # 最新を取り込むため一旦Pull
    o = repo.remotes.origin
    o.pull()
    repo.git.reset("--hard", "origin/main")  # リモートのmainにハードリセット


def process_task_folder(task_folder):
    print("process_task_folder")
    # タスクフォルダの処理
    readme_path = os.path.join(task_folder, README_FILENAME)
    with open(readme_path, "r") as f:
        content = f.read()

    # Readmeから情報を抽出
    send_path = content.split(SEND_PATH_KEY)[1].split('"')[0]
    target_file = content.split(TARGET_FILE_KEY)[1].split('"')[0]

    # ファイルの移動
    print("folder_move")
    task_name = os.path.basename(task_folder)  # task_folderの名前を取得
    destination_path = os.path.join(
        send_path, task_name
    )  # send_pathの直下に移動するパスを作成
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)  # ディレクトリを削除
    shutil.move(task_folder, send_path)  # task_folderをsend_pathの直下に移動

    # MATLABの実行
    print("MATLABの実行")
    matlab_cmd = f"matlab -nosplash -nodesktop -r \"cd('{destination_path}'); run('{target_file}'); exit;\""
    # MATLABをGUIで実行
    matlab_process = subprocess.Popen(matlab_cmd, shell=True)

    # MATLABの処理が終わるまで待機
    time.sleep(10)
    print("MATLAB起動中")
    matlab_process.wait()  # MATLABプロセスが終了するのを待つ
    print("MATLAB終了")
    # akaan

    # 30秒待機zyouhoutokeikokunikannsuru
    print("30秒待機中")
    time.sleep(25)
    return send_path


def move_push_repository(repo_path, task_folder, send_path):
    # ファイルの移動
    print("folder_move")
    task_name = os.path.basename(task_folder)  # task_folderの名前を取得
    destination_path = os.path.join(send_path, task_name)

    print("push_repository")
    # リポジトリにプッシュ
    os.chdir(repo_path)
    repo = git.Repo()
    # 最新を取り込むため一旦Pull
    print("pull_repository")
    o = repo.remotes.origin
    o.pull()
    repo.git.reset("--hard", "origin/main")  # リモートのmainにハードリセット

    # 結果の移動
    print("結果の移動")
    task_name = os.path.basename(task_folder)
    results_path = os.path.join(destination_path, "results")
    destination_dir = os.path.join(RESULTS_PATH, task_name)

    # 既存のディレクトリを削除してから作成
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)  # 既存のディレクトリを削除
    os.makedirs(destination_dir)  # 新しいディレクトリを作成
    for item in os.listdir(results_path):
        source_item = os.path.join(results_path, item)
        source_item = MatDevider.MatDevider.split_mat_file(source_item)
        shutil.move(source_item, destination_dir)

    repo.git.add(A=True)
    print("commit_repository")
    repo.git.commit(".", "-m", '"Commit Log"')

    # Push
    origin = repo.remote(name="origin")
    print("push_repository")
    try:
        origin.push(force=True)  # 強制的にプッシュ
    except Exception as e:
        print(f"プッシュ中にエラーが発生しました: {e}")


def main():
    while True:
        random_wait()

        pull_repository(REPO_PATH)
        # MATLABプロセスが動作していない、かつタスクフォルダが存在する場合
        if not (check_matlab_process()) and os.listdir(TASKS_PATH):
            task_folder = os.path.join(TASKS_PATH, os.listdir(TASKS_PATH)[0])
            send_path = process_task_folder(task_folder)
            move_push_repository(REPO_PATH, task_folder, send_path)


if __name__ == "__main__":
    main()
