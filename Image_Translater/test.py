import tkinter as tk


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1098x1400+758+50")

        # メインウィンドウの設定
        self.root.wm_attributes("-transparentcolor", "white")
        self.frame = tk.Frame(self.root, background="white")
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.root.wm_title("Get Size Window")

        # 初期サイズを保存
        self.prev_width = self.root.winfo_width()
        self.prev_height = self.root.winfo_height()

        # ウィンドウのサイズが変更されたときのみ呼び出すイベントバインディング
        self.root.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()

        # サイズが変更された場合のみ処理
        if new_width != self.prev_width or new_height != self.prev_height:
            self.prev_width = new_width
            self.prev_height = new_height

            # 新しいサイズと位置でウィンドウを再作成
            new_x = self.root.winfo_rootx()
            new_y = self.root.winfo_rooty()
            self.root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
