import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo
import subprocess


class GitHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            relative_path = os.path.relpath(file_path, self.repo_path)
            print(f"新しいファイルが検出されました: {relative_path}")

            # 追加: .git ディレクトリ内のファイルを無視する
            if relative_path.startswith(".git/"):
                print(f"{relative_path} は無視されました")
                return

            # Gitに新しいファイルを追加
            self.repo.index.add([relative_path])

            # コミットを作成
            self.repo.index.commit(f"新しいファイルを追加: {relative_path}")

            # リモートにプッシュ
            origin = self.repo.remote("origin")
            origin.push()

            print(f"{relative_path} がリモートリポジトリに追加されました")


def pull_and_add_new_files(repo):
    print("リモートからプルしています...")
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
    repo_path = r"C:\prog\kawa_matlab"
    repo = Repo(repo_path)

    # 初期プルと新ファイルの追加
    pull_and_add_new_files(repo)

    event_handler = GitHandler(repo_path)
    observer = Observer()
    observer.schedule(event_handler, repo_path, recursive=True)
    observer.start()

    try:
        print("ファイルシステムの監視を開始しました...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
