import os
import time
import random
import shutil
import git
import MatDevider
import socket
import matlab.engine
import datetime
import sys

# 文字列定数
MATLAB_PROCESS_NAME = "MATLAB.exe"
README_FILENAME = "Readme.txt"
SEND_PATH_KEY = 'Send Path = "'
TARGET_FILE_KEY = 'Target File = "'
RESULTS_PATH_KEY = 'Results Path = "'
COMMIT_MESSAGE = "Task completed and results added"
STOP_FILE = "stop.txt"


def get_exe_directory():
    if getattr(sys, "frozen", False):
        # exeファイルとして実行されている場合
        return os.path.dirname(sys.executable)
    else:
        # 通常のPythonスクリプトとして実行されている場合
        return os.path.dirname(os.path.abspath(__file__))


#  各PCに対応したパスの設定
def process_path(input_string):
    # Usersディレクトリのパスを設定
    users_path = "/Users"

    # Usersディレクトリ内のユーザーディレクトリを取得
    user_dirs = [
        d for d in os.listdir(users_path) if os.path.isdir(os.path.join(users_path, d))
    ]

    # 特殊なシステムディレクトリを除外
    system_dirs = ["Shared", "Guest", "共有", "ゲスト"]
    user_dirs = [d for d in user_dirs if d not in system_dirs]
    user_name = user_dirs[0]

    # 入力文字列をカンマで分割
    paths = input_string.split(",")

    # 結果を格納するリスト
    result = []

    for path in paths:
        # パスを'/'で分割し、2番目の要素（インデックス1）を現在のユーザー名に置換
        path_parts = path.split("/")
        path_parts[2] = user_name
        result.append("/".join(path_parts))

    # 結果をカンマで結合して返す
    return ",".join(result)


# ObservePath.txtファイルを読み込み各種パス、ディレクトリの設定を行う関数
def load_observe_path():

    global REPO_PATH
    global TASKS_PATH
    global RESULTS_PATH
    global MATLAB_WORK_DIR

    # カレントディレクトリのObservePath.txtファイルのパスを取得
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "ObservePath.txt")

    # ファイルが存在するか確認
    if not os.path.exists(file_path):
        print("ObservePath.txtファイルが見つかりません。")
        return

    # 変数の初期化
    repo_paths = []
    matlab_work_dirs = []

    # ファイルを読み込み、各行を処理
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # '='で分割し、変数名と値を取得
            parts = line.strip().split("=")
            if len(parts) == 2:
                var_name, var_value = parts
                var_name = var_name.strip()
                var_value = var_value.strip().strip("[").strip("]").split(",")

                # 配列として解釈し、リストに追加
                if var_name == "REPO_PATH":
                    repo_paths = var_value
                elif var_name == "MATLAB_WORK_DIR":
                    matlab_work_dirs = var_value

    # ランダムに要素を選択
    num_list = list(range(len(repo_paths)))
    if repo_paths and matlab_work_dirs:
        if len(repo_paths) == len(matlab_work_dirs) and len(repo_paths) > 0:
            num_random = random.choice(num_list)
            REPO_PATH = process_path(repo_paths[num_random])
            MATLAB_WORK_DIR = process_path(matlab_work_dirs[num_random])
        else:
            print("REPO_PATH,MATLAB_WORK_DIRが適切に定義されていません。")
            return
    else:
        print("REPO_PATH,MATLAB_WORK_DIRが適切に定義されていません。")
        return

    # PCの名前を取得
    pc_name = socket.gethostname().split(".")[0]

    # 定数の定義
    pc_path = os.path.join(REPO_PATH, pc_name)
    TASKS_PATH = os.path.join(REPO_PATH, f"{pc_name}/tasks")  # PC名を含めたパス
    RESULTS_PATH = os.path.join(REPO_PATH, f"{pc_name}/results")  # PC名を含めたパス

    # フォルダが存在しない場合は作成
    os.makedirs(pc_path, exist_ok=True)
    os.makedirs(TASKS_PATH, exist_ok=True)
    os.makedirs(RESULTS_PATH, exist_ok=True)

    print(f"選択されたREPO_PATH: {REPO_PATH}")
    print(f"選択されたMATLAB_WORK_DIR: {MATLAB_WORK_DIR}")


# リポジトリをプル
def pull_repository():
    print("pull_repository")
    os.chdir(REPO_PATH)
    repo = git.Repo()
    # 最新を取り込むため一旦Pull
    o = repo.remotes.origin
    o.pull()
    repo.git.reset("--hard", "head")  # リモートのmainにハードリセット


# リポジトリをプッシュ
def push_repository(task_name):
    try:
        os.chdir(REPO_PATH)
        repo = git.Repo()
        repo.git.add(A=True)
        print("commit_repository")
        repo.git.commit(".", "-m", '"Commit Log"')
        origin = repo.remote(name="origin")
        print("push_repository")
        origin.push(force=True)  # 強制的にプッシュ
    except Exception as e:
        print(f"プッシュ中にエラーが発生しました: {e}")
        make_empty_file = os.path.join(RESULTS_PATH, task_name + "_errorlog.txt")
        f = open(make_empty_file, "w")
        now = datetime.datetime.now()
        f.write(f"プッシュ中にエラーが発生しました。\n")
        formatted_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
        f.write(f"{formatted_time}\n")
        f.close()  # リモートのmainにハードリセット


# matlabの実行のためのファイル移動と実行
def process_task_folder(task_folder):
    global TASK_NAME
    print("process_task_folder")

    TASK_NAME = os.path.basename(task_folder)
    # results_path = os.path.join(destination_path, "results")
    # destination_dir = os.path.join(RESULTS_PATH, task_name)
    readme_path = os.path.join(task_folder, README_FILENAME)
    try:
        print("folder_move")
        with open(readme_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        # ファイルの移動
        print("error_folder_move")
        destination_path = os.path.join(
            RESULTS_PATH, TASK_NAME
        )  # send_pathの直下に移動するパスを作成
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)  # ディレクトリを削除
        shutil.move(task_folder, RESULTS_PATH)  # task_folderをsend_pathの直下に移動
        task_folder = os.path.join(RESULTS_PATH, TASK_NAME)
        return task_folder

    # Readmeから情報を抽出
    send_path = process_path(
        content.split(SEND_PATH_KEY)[1].split('"')[0].replace("\\", "/")
    )
    target_file = content.split(TARGET_FILE_KEY)[1].split('"')[0].replace("\\", "/")

    # ファイルの移動
    print("folder_move")
    destination_path = os.path.join(
        send_path, TASK_NAME
    )  # send_pathの直下に移動するパスを作成
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)  # ディレクトリを削除
    shutil.move(task_folder, destination_path)  # task_folderをsend_pathの直下に移動

    print("MATLABの実行")
    # MATLABエンジンを起動
    eng = matlab.engine.start_matlab()
    eng.cd(destination_path, nargout=0)
    eng.run(target_file, nargout=0)
    time.sleep(10)  # 10秒待機
    task_folder = os.path.join(send_path, TASK_NAME)

    return task_folder


# 実行後のファイルの移動とGitに上げる処理
def move_push_repository(task_folder, send_path):
    print("folder_move")
    task_name = os.path.basename(task_folder)  # task_folderの名前を取得
    destination_path = os.path.join(send_path, task_name)

    print("push_repository")
    # リポジトリにプッシュ
    os.chdir(REPO_PATH)
    repo = git.Repo()
    # 最新を取り込むため一旦Pull
    print("pull_repository")
    o = repo.remotes.origin
    o.pull()
    repo.git.reset("--hard", "origin/main")  # リモートのmainにハードリセット

    # 結果の移動
    print("結果の移動")
    # 既存のディレクトリを削除してから作成
    task_folder_results = os.path.join(task_folder, "results")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)  # 既存のディレクトリを削除
    old_task_folder = os.path.join(TASKS_PATH, TASK_NAME)
    if os.path.exists(old_task_folder):
        shutil.rmtree(old_task_folder)  # 元のディレクトリを削除
    try:
        if os.listdir(task_folder_results):
            for item in os.listdir(task_folder_results):
                source_item = os.path.join(task_folder_results, item)
                # Matファイルの分割(Githubのファイルサイズ制限対策)
                temp_source_item = MatDevider.MatDevider.split_mat_file(source_item)
                if temp_source_item:
                    source_item = temp_source_item
            shutil.move(task_folder, RESULTS_PATH)
        else:
            os.makedirs(destination_path)
            make_empty_file = os.path.join(
                destination_path, task_name + "_errorlog.txt"
            )
            f = open(make_empty_file, "w")
            now = datetime.datetime.now()
            f.write(f"出力結果がありません。\n")
            formatted_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
            f.write(f"{formatted_time}\n")
            f.close()
    except Exception as e:
        print(f"結果の移動中にエラーが発生しました: {e}")

    push_repository(task_name)


def main():
    original_dir = get_exe_directory()
    os.chdir(original_dir)
    print(f"現在のカレントディレクトリ: {original_dir}")
    load_observe_path()
    pull_repository()
    load_observe_path()
    # tasksフォルダにmemo.txtを作成(Githubに空のフォルダをプッシュするため)
    memo_file_path = os.path.join(TASKS_PATH, "memo.txt")
    with open(memo_file_path, "w") as f:
        pass  # 空のファイルを作成
    push_repository("Initial commit")

    # メインループ　Gitリポジトリの更新を監視し、matlabを実行
    while True:
        os.chdir(original_dir)
        print("待機中...")
        time.sleep(60)
        load_observe_path()
        try:
            pull_repository()
        except Exception as e:
            print(f"リポジトリの取得中にエラーが発生しました: {e}")
            continue
        os.chdir(TASKS_PATH)
        folders = [
            f
            for f in os.listdir(TASKS_PATH)
            if os.path.isdir(os.path.join(TASKS_PATH, f))
        ]
        if folders:
            task_folder = os.path.join(TASKS_PATH, folders[0])
            task_folder = process_task_folder(task_folder)
            move_push_repository(task_folder, RESULTS_PATH)


if __name__ == "__main__":
    main()
