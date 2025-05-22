import tkinter as tk
import os
import re

# スクショ撮影範囲の記録テキストのパス
path = r"C:\prog\Python\Python_Github\Image_Translater\size.txt"
# スクショ撮影範囲の初期位置
default_window_size = "1098x1400+758+50"


class Size_Reference_Window:
    def __init__(self, root):
        self.root = root
        window_size = default_window_size

        # スクショ撮影範囲の記録テキストにサイズ情報が格納されているかチェック
        pattern = re.compile(r"^\d+x\d+([+-]\d+){2}$")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                window_size_text = file.read().strip()
                pattern = re.compile(r"^\d+x\d+([+-]\d+){2}$")
                if bool(pattern.match(window_size_text)):
                    window_size = window_size_text

        # ウィンドウの初期サイズと位置を設定
        self.root.geometry(window_size)

        # メインウィンドウの設定
        self.root.wm_attributes("-transparentcolor", "white")
        self.frame = tk.Frame(
            self.root,
            background="white",
            highlightbackground="black",
            highlightthickness=2,
        )
        self.frame.place(
            x=0, y=0, relwidth=1, relheight=1
        )  # フレームをウィンドウ全体に広げる
        self.root.wm_title("Get Size Window")

        # ウィンドウのサイズが変更されたときのみ呼び出すイベントバインディング
        self.root.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        # ウィンドウの新しいサイズと位置を取得
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        new_x = self.root.winfo_rootx()
        new_y = self.root.winfo_rooty()

        # フレームのサイズをウィンドウサイズより一回り小さく設定
        frame_width = new_width - 20  # ウィンドウより20ピクセル小さい
        frame_height = new_height - 60  # ウィンドウより60ピクセル小さい
        self.frame.config(width=frame_width, height=frame_height)

        # 新しいウィンドウサイズと位置をスクショ撮影範囲の記録テキストに保存
        window_size = f"{new_width}x{new_height}+{new_x}+{new_y}"
        with open(path, "w", encoding="utf-8") as file:
            file.write(window_size)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MainApp(root)
#     root.mainloop()
