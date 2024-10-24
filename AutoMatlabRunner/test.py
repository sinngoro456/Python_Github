import os

def create_folders():
    # カレントディレクトリを取得
    current_dir = os.getcwd()
    print(f"現在のディレクトリ: {current_dir}")

    # カレントディレクトリに新しいフォルダを作成
    new_folder_current = "new_folder_current"
    try:
        os.mkdir(new_folder_current)
        print(f"カレントディレクトリに '{new_folder_current}' フォルダを作成しました。")
    except FileExistsError:
        print(f"'{new_folder_current}' フォルダは既に存在します。")

    # 一つ上のディレクトリに新しいフォルダを作成
    parent_dir = os.path.dirname(current_dir)
    new_folder_parent = "new_folder_parent"
    parent_new_folder_path = os.path.join(parent_dir, new_folder_parent)
    
    try:
        os.mkdir(parent_new_folder_path)
        print(f"親ディレクトリに '{new_folder_parent}' フォルダを作成しました。")
    except FileExistsError:
        print(f"'{new_folder_parent}' フォルダは既に親ディレクトリに存在します。")
    except PermissionError:
        print(f"権限エラー: 親ディレクトリに '{new_folder_parent}' フォルダを作成できません。")

if __name__ == "__main__":
    create_folders()