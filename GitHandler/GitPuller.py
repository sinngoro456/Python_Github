

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo

# 監視対象のパスを設定
REPO_PATH = r"/Users/kawabuchy/Public/Github_test"


class GitHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.repo_path = path
        self.repo = Repo(path)  # 変数名を repo から repo_instance に変更
        self.cooldown = 1  # クールダウン時間（秒）

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            relative_path = os.path.relpath(file_path, self.repo_path)

            # .git ディレクトリ内のファイルを無視する
            if relative_path.startswith(".git"):
                return

            print(f"新しいファイルが検出されました: {relative_path}")

            # クールダウン待機
            time.sleep(self.cooldown)

            try:
                # ファイルが存在するか確認
                if os.path.exists(file_path):
                    # Gitに新しいファイルを追加
                    self.repo.index.add([relative_path])

                    # コミットを作成
                    self.repo.index.commit(f"新しいファイルを追加: {relative_path}")

                    # リモートにプッシュ
                    origin = self.repo.remote("origin")
                    origin.push()

                    print(f"{relative_path} がリモートリポジトリに追加されました")
                else:
                    print(f"警告: ファイル {relative_path} が見つかりません")
            except Exception as e:
                print(
                    f"エラー: {relative_path} の処理中に問題が発生しました - {str(e)}"
                )

    def on_modified(self, event):
        # 必要に応じて、ファイルの変更を処理するロジックをここに追加
        pass

    def on_deleted(self, event):
        if not event.is_directory:
            relative_path = os.path.relpath(event.src_path, self.repo_path)

            # .git ディレクトリ内のファイルを無視する
            if relative_path.startswith(".git"):
                return

            print(f"ファイルが削除されました: {relative_path}")

            # クールダウン待機
            time.sleep(self.cooldown)

            try:
                # Gitからファイルを削除
                self.repo.index.remove([relative_path])

                # コミットを作成
                self.repo.index.commit(f"ファイルを削除: {relative_path}")

                # リモートにプッシュ
                origin = self.repo.remote("origin")
                origin.push()

                print(f"{relative_path} がリモートリポジトリから削除されました")
            except Exception as e:
                print(
                    f"エラー: {relative_path} の削除処理中に問題が発生しました - {str(e)}"
                )


def pull_and_add_new_files(repo):
    print("リモートからプルしています...")

    # ローカルの変更をコミット
    if repo.is_dirty() or repo.untracked_files:
        repo.git.add(A=True)
        repo.index.commit("自動コミット: ローカルの変更")

    origin = repo.remote("origin")
    origin.pull()

    # 新しいファイルを検出して追加
    untracked_files = repo.untracked_files
    if untracked_files:
        print("新しいファイルを追加しています...")
        repo.index.add(untracked_files)
        repo.index.commit("新しいファイルを追加")
        origin.push()
        print(f"{len(untracked_files)}個の新しいファイルが追加されました")
    else:
        print("新しいファイルはありません")


if __name__ == "__main__":
    repo_instance = Repo(REPO_PATH)  # 変数名を repo から repo_instance に変更

    # 初期プルと新ファイルの追加
    pull_and_add_new_files(repo_instance)  # 変数名を repo から repo_instance に変更

    event_handler = GitHandler(REPO_PATH)
    observer = Observer()
    observer.schedule(event_handler, REPO_PATH, recursive=True)
    observer.start()

    try:
        print("ファイルシステムの監視を開始しました...")
        count = 0
        while True:
            time.sleep(1)
            if count > 10:
                print("リモートからプルしています...")
                pull_and_add_new_files(REPO_PATH)
                count = 0
            else:
                count = count + 1

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
