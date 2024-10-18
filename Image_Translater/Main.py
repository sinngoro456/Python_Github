import threading
import tkinter as tk
import Size_Reference_Window as SRW
import Screenshot_and_Translate as MST
import time


class Translater:
    def __init__(self):
        self.stop_event = threading.Event()

    # スクショ範囲参照用ウィンドウ作成関数
    def Size_Reference_Window(self):
        root1 = tk.Tk()

        def check_stop_event():
            if self.stop_event.is_set():  # ストップイベントがセットされているか確認
                root1.destroy()  # ウィンドウを閉じる
                return  # 監視を終了
            root1.after(1000, check_stop_event)  # 1000ミリ秒後に再度チェック

        SRW.Size_Reference_Window(root1)
        check_stop_event()  # 監視を開始
        root1.mainloop()
        self.stop_event.set()
        print("Size_Reference_Window 終了")

    # 指定範囲のスクショを撮影して翻訳する関数
    def Main_Screenshot_and_Translate(self):
        root2 = tk.Tk()

        def check_stop_event():
            if self.stop_event.is_set():  # ストップイベントがセットされているか確認
                root2.destroy()  # ウィンドウを閉じる
                return  # 監視を終了
            root2.after(1000, check_stop_event)  # 1000ミリ秒後に再度チェック

        translator = MST.OCRTranslator()
        time.sleep(0.05)
        flag = True
        while flag:
            flag = False
            check_stop_event()
            flag = translator.translate_from_screenshot(root2)
        self.stop_event.set()
        print("Main_Screenshot_and_Translate 終了")


# メイン
if __name__ == "__main__":
    translater = Translater()

    # ウィンドウ表示関数root.mainloop()が処理を止めてる間も並行して処理を行いたいのでマルチスレッドで並行して処理を行う
    # スレッドを作る
    thread1 = threading.Thread(target=translater.Size_Reference_Window)
    thread2 = threading.Thread(target=translater.Main_Screenshot_and_Translate)

    # スレッドの処理を開始
    thread1.start()
    thread2.start()

    # スレッドの処理を待つ
    thread1.join()
    thread2.join()
