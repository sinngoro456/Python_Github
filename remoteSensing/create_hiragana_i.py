import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams["font.family"] = "Hiragino Sans"

# ファイル名の指定
output_dir = "tomography_results"
os.makedirs(output_dir, exist_ok=True)

# ひらがなの「い」の画像を作成
def create_hiragana_i(size=64):
    img = np.zeros((size, size))
    img[20:50, 20:25] = 1  # 縦線
    img[45:50, 20:45] = 1  # 横線
    return img

# 円形の画像を作成
def create_circle(size=64):
    x, y = np.ogrid[:size, :size]
    center = size / 2
    radius = size / 4
    circle = ((x - center)**2 + (y - center)**2 <= radius**2).astype(float)
    return circle

# 複数の四角形を含む画像を作成
def create_squares(size=64):
    img = np.zeros((size, size))
    img[10:20, 10:20] = 1
    img[40:55, 40:55] = 1
    img[15:25, 45:55] = 1
    return img

# 画像の表示と保存関数
def display_and_save_image(img, title):
    plt.figure()
    plt.imshow(img, cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.savefig(os.path.join(output_dir, f"{title}.png"))
    plt.close()

# 投影データの生成
def generate_projections(image, num_angles=180):
    size = image.shape[0]
    angles = np.linspace(0, np.pi, num_angles, endpoint=False)
    A = np.zeros((num_angles * size, size * size))

    for i, angle in enumerate(angles):
        cos_rot, sin_rot = np.cos(angle), np.sin(angle)
        for j in range(size):
            x = np.arange(size) - size // 2
            y = j - size // 2
            proj = x * cos_rot + y * sin_rot + size // 2
            proj = np.clip(proj, 0, size - 1).astype(int)
            A[i * size + j, proj + y * size] = 1

    x = image.flatten()
    sinogram = (A @ x).reshape(size, num_angles)

    return sinogram, A

def analytical_solution(A, sinogram):
    y = sinogram.flatten()
    x = np.linalg.pinv(A) @ y
    return x.reshape(sinogram.shape[0], sinogram.shape[0])

def kaczmarz_method(A, sinogram, num_iterations=100):
    y = sinogram.flatten()
    x = np.zeros(A.shape[1])
    for _ in range(num_iterations):
        for i in range(len(y)):
            a_i = A[i]
            x += (y[i] - np.dot(a_i, x)) / np.dot(a_i, a_i) * a_i
    return x.reshape(sinogram.shape[0], sinogram.shape[0])

def soft_threshold(x, g):
    return np.sign(x) * np.maximum(np.abs(x) - g, 0)

def l1_norm_minimization(A, sinogram, num_iterations=1000, learning_rate=0.0001, lambda_reg=0.1):
    y = sinogram.flatten()
    x = np.zeros(A.shape[1])
    for _ in range(num_iterations):
        gradient = 2 * A.T @ (A @ x - y)
        x_next = x - learning_rate * gradient
        x = soft_threshold(x_next, lambda_reg * learning_rate)
    return x.reshape(sinogram.shape[0], sinogram.shape[0])

# 画像の生成と処理
for create_func, name in [(create_hiragana_i, "hiragana_i"), (create_circle, "circle"), (create_squares, "squares")]:
    original_image = create_func()
    display_and_save_image(original_image, f"元画像_{name}")

    sinogram, A = generate_projections(original_image, 180)
    display_and_save_image(sinogram, f"サイノグラム_{name}")

    reconstructed_analytical = analytical_solution(A, sinogram)
    display_and_save_image(reconstructed_analytical, f"解析解による再構成画像_{name}")

    reconstructed_kaczmarz = kaczmarz_method(A, sinogram)
    display_and_save_image(reconstructed_kaczmarz, f"Kaczmarz法による再構成画像_{name}")

    reconstructed_l1 = l1_norm_minimization(A, sinogram)
    display_and_save_image(reconstructed_l1, f"L1ノルム最小化による再構成画像_{name}")

print(f"結果は {output_dir} ディレクトリに保存されました。")
