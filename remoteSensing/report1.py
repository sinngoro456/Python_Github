import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.fftpack import fft2, ifft2
from tkinter import Tk, filedialog


# 画像の読み込み
def load_image(file_path):
    if file_path:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # グレースケール変換
        if image is None:
            print("Error: Could not load image. Please try a different file.")
        return image
    else:
        print("No file selected.")
        return None


# ピンボケフィルターの作成
def create_blur_kernel(size=5):
    kernel = np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 2, 2, 2, 1],
            [1, 2, 3, 2, 1],
            [1, 2, 2, 2, 1],
            [1, 1, 1, 1, 1],
        ],
        dtype=np.float32,
    )
    kernel /= np.sum(kernel)  # 正規化
    return kernel


# 画像にフィルターを適用してピンボケを作成
def apply_blur(image, kernel):
    return convolve2d(image, kernel, mode="same", boundary="symm")


# ガウスノイズを追加
def add_noise(image, sigma=100):
    noise = np.random.normal(0, sigma, image.shape)
    return np.clip(image + noise, 0, 255)  # 値を0~255にクリップ


# フーリエ変換を利用してチホノフ正則化を適用
def tikhonov_deblurring(noisy_blurred_image, kernel, lambda_reg=10000):
    image_size = noisy_blurred_image.shape  # 画像のサイズを取得
    kernel_padded = np.zeros(image_size)  # 画像サイズと同じゼロパディングカーネルを作成
    kh, kw = kernel.shape  # カーネルの高さ・幅

    kernel_padded[:kh, :kw] = kernel
    F_blurred = fft2(noisy_blurred_image)  # 画像のフーリエ変換
    F_kernel = fft2(kernel_padded)  # ゼロパディングしたカーネルのフーリエ変換
    F_deblurred_tikhonov = (
        F_blurred * np.conj(F_kernel) / (np.abs(F_kernel) ** 2 + lambda_reg)
    )
    return np.real(ifft2(F_deblurred_tikhonov))


# 画像処理のメイン関数
def process_image():
    file_path = "/Users/kawabuchy/Downloads/mountains-9092630_1280.jpg"
    if not file_path:
        return

    image = load_image(file_path)
    if image is None:
        return

    kernel = create_blur_kernel()
    blurred_image = apply_blur(image, kernel)
    noisy_blurred_image = add_noise(blurred_image)
    deblurred_tikhonov = tikhonov_deblurring(noisy_blurred_image, kernel)

    # 結果の表示
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Original Image")
    axes[1].imshow(blurred_image, cmap="gray")
    axes[1].set_title("Blurred Image")
    axes[2].imshow(noisy_blurred_image, cmap="gray")
    axes[2].set_title("Noisy Blurred Image")
    axes[3].imshow(deblurred_tikhonov, cmap="gray")
    axes[3].set_title("Deblurred Image (Tikhonov)")
    plt.show()


# 実行
if __name__ == "__main__":
    process_image()
