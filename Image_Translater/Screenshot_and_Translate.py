import os
import tkinter as tk
import pyocr
import pyautogui
import re
import deepl
from googletrans import Translator
import pyperclip
import pygetwindow as gw

# DeepL 設定
API_KEY = "ee58b7b7-459f-4b79-826b-384aa3be18ac:fx"  # 自身の API キーを指定

source_lang = "EN"
target_lang = "JA"

# 画像→文字の設定
TESSERACT_PATH = (
    "C:\\Program Files\\Tesseract-OCR"  # インストールしたTesseract-OCRのpath
)
TESSDATA_PATH = "C:\\Program Files\\Tesseract-OCR\\tessdata"  # tessdataのpath

os.environ["PATH"] += os.pathsep + TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

tools = pyocr.get_available_tools()
tool = tools[0]

# Google翻訳 設定
translator = Translator()


class OCRTranslator:
    def __init__(self):
        self.tool = tool
        self.translator = deepl.Translator(API_KEY)
        self.text_widget_left = None
        self.text_widget_right = None
        self.root = None

    def replace_newlines(self, text):
        # 2つ以上の連続する改行でテキストを分割
        items = re.split(r"\n", text.strip())
        # 日本語の文字を含まない要素のみをフィルタリング
        filtered_items = [
            item if not re.search(r"[ぁ-んァ-ン一-龥]", item) else r"__DOUBLE_NEWLINE__"
            for item in items
        ]
        text = "".join(filtered_items)
        # ,
        # 連続する改行・スペースを半角スペースに置換
        text = re.sub(r"\s+", " ", text)
        # text = re.sub(".", "\n", text)
        text = re.sub(r"\n", r"\n\n", text)
        text = re.sub(r"__DOUBLE_NEWLINE__", "\n\n", text)
        text = re.sub(r"(OA|0A)", r"\n\nOA", text)
        text = re.sub(r"(OC|0C|Oc|0c)", r"OC\n", text)
        text = re.sub(
            r"information.",
            r"information.\n\n\n",
            text,
        )
        text = re.sub(
            r"(AThe statement|A.The statement)",
            r"\n\n\n\nA.The statement",
            text,
        )
        return text.lstrip()

    # スクショ範囲参照用ウィンドウの範囲取得関数
    def get_window_info(self, window_title):
        try:
            # 指定したタイトルを持つウィンドウを取得
            window = gw.getWindowsWithTitle(window_title)[0]

            # ウィンドウの位置とサイズを取得
            left = window.left
            top = window.top
            width = window.width
            height = window.height

            return [left, top + 70, width, height - 70]

        except IndexError:
            print(f"タイトル '{window_title}' のウィンドウが見つかりませんでした。")
            return [758, 255, 1098, 1098]
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return [758, 255, 1098, 1098]

    def render_doc_text(self, img):
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        text = self.tool.image_to_string(img, lang="jpn", builder=builder)
        output_text = self.replace_newlines(text)
        pyperclip.copy(output_text)
        return output_text

    def display_dual_texts(self, root, text_left, text_right):
        print("display_dual_texts")
        self.root = root
        self.root.geometry("1600x1000-2700+600")
        self.root.title("OCR翻訳ツール")
        self.root.configure(bg="#f0f0f0")  # 背景色を設定

        # メインフレーム
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 翻訳ボタンを上部に配置
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(side="top", fill="x", pady=(0, 10))

        translate_button = tk.Button(
            button_frame,
            text="翻訳",
            command=self.update_translation,
            bg="#4CAF50",  # ボタンの背景色
            fg="white",  # ボタンのテキスト色
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=10,
        )
        translate_button.pack()

        # テキストフレーム
        text_frame = tk.Frame(main_frame, bg="#f0f0f0")
        text_frame.pack(side="top", fill="both", expand=True)

        # 左側のテキストフレーム
        frame_left = tk.Frame(text_frame, bg="#f0f0f0")
        frame_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.text_widget_left = tk.Text(frame_left, wrap="char", font=("Helvetica", 11))
        self.text_widget_left.pack(fill="both", expand=True)

        scrollbar_left = tk.Scrollbar(frame_left, command=self.text_widget_left.yview)
        scrollbar_left.pack(side="right", fill="y")
        self.text_widget_left.config(yscrollcommand=scrollbar_left.set)

        self.text_widget_left.insert("1.0", text_left)

        # 右側のテキストフレーム
        frame_right = tk.Frame(text_frame, bg="#f0f0f0")
        frame_right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.text_widget_right = tk.Text(
            frame_right, wrap="char", font=("Helvetica", 11)
        )
        self.text_widget_right.pack(fill="both", expand=True)

        scrollbar_right = tk.Scrollbar(
            frame_right, command=self.text_widget_right.yview
        )
        scrollbar_right.pack(side="right", fill="y")
        self.text_widget_right.config(yscrollcommand=scrollbar_right.set)

        self.text_widget_right.insert("1.0", text_right)

        # ラベルの追加
        tk.Label(
            frame_left, text="原文", bg="#f0f0f0", font=("Helvetica", 12, "bold")
        ).pack(side="top", pady=(0, 5))
        tk.Label(
            frame_right, text="翻訳", bg="#f0f0f0", font=("Helvetica", 12, "bold")
        ).pack(side="top", pady=(0, 5))

        self.root.mainloop()

    def update_translation(self):
        print("翻訳ボタンが押されました。")
        # 新しいスクリーンショットを撮影
        output_path = r"C:\prog\Python\Python_Github\Image_Translater\output_image.jpg"
        [left, top, width, height] = self.get_window_info("Get Size Window")
        cropped_img = pyautogui.screenshot(
            output_path, region=(left, top, width, height)
        )

        # 新しいテキストを取得
        new_text = self.render_doc_text(cropped_img)
        if not new_text:
            new_text = "none"

        # 新しいテキストを翻訳
        new_text_translated = self.translator.translate_text(
            new_text, source_lang=source_lang, target_lang=target_lang
        ).text

        # テキストウィジェットの内容を更新
        self.text_widget_left.delete("1.0", tk.END)
        self.text_widget_left.insert("1.0", new_text)

        self.text_widget_right.delete("1.0", tk.END)
        self.text_widget_right.insert("1.0", new_text_translated)

        return True

    def translate_from_screenshot(
        self, root, left=-1500, top=0, width=2000, height=1400
    ):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        output_path = r"C:\prog\Python\Python_Github\Image_Translater\output_image.jpg"

        [left, top, width, height] = self.get_window_info("Get Size Window")

        cropped_img = pyautogui.screenshot(
            output_path, region=(left, top, width, height)
        )
        text = self.render_doc_text(cropped_img)
        if not text:
            text = "none"
        text_translated_deepl = self.translator.translate_text(
            text, source_lang=source_lang, target_lang=target_lang
        ).text
        self.display_dual_texts(root, text, text_translated_deepl)

        ## google翻訳も入れたい場合はこれをコメントアウト。APIの認証情報は各自で。
        # text_translated_google = self.translate_google(text)  # デフォルトでは英語へ変換
        # self.display_triple_texts(text, text_translated_deepl, text_translated_google)


# # メイン処理
# if __name__ == "__main__":
#     translator = OCRTranslator()

#     translator.translate_from_screenshot(left=700, top=500, width=1000, height=900)

#     for _ in range(10):
#         translator.translate_from_screenshot(left=700, top=500, width=1000, height=900)

#     print("a")
#     sys.exit()
