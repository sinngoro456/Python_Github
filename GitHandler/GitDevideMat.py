import os
import scipy.io as sio
import time

class MatDevider:
    @staticmethod
    def is_mat_file(file_path):
        """ファイルがMATファイルかどうかを判定する"""
        try:
            sio.loadmat(file_path, verify_compressed_data_integrity=False)
            return True
        except:
            return False

    @staticmethod
    def split_mat_file(input_mat_file, output_directory, chunk_size_mb=500):
        if not MatDevider.is_mat_file(input_mat_file):
            raise ValueError(f"入力ファイル {input_mat_file} はMATファイルではありません。")

        start_time = time.time()
        
        if not os.path.exists(input_mat_file):
            raise FileNotFoundError(f"入力ファイル {input_mat_file} が見つかりません。")

        base_filename = os.path.splitext(os.path.basename(input_mat_file))[0]
        
        output_subdirectory = os.path.join(output_directory, base_filename)
        if not os.path.exists(output_subdirectory):
            os.makedirs(output_subdirectory)

        print(f"ファイル {input_mat_file} の読み込みを開始します...")
        mat_data = sio.loadmat(input_mat_file)
        print(f"ファイルの読み込みが完了しました。経過時間: {time.time() - start_time:.2f}秒")

        chunk_size_bytes = chunk_size_mb * 1024 * 1024
        var_names = [key for key in mat_data.keys() if not key.startswith('__')]

        chunk_data = {}
        current_chunk_size = 0
        chunk_number = 1
        total_size = 0

        for var_name in var_names:
            var_size = mat_data[var_name].nbytes
            total_size += var_size

            chunk_data[var_name] = mat_data[var_name]
            current_chunk_size += var_size

            if current_chunk_size >= chunk_size_bytes:
                output_file = os.path.join(output_subdirectory, f"{base_filename}_{chunk_number}.mat")
                sio.savemat(output_file, chunk_data)
                print(f"チャンク {chunk_number} を保存しました: {output_file}")
                print(f"チャンクサイズ: {current_chunk_size / (1024 * 1024):.2f} MB")

                chunk_data = {}
                current_chunk_size = 0
                chunk_number += 1

        if chunk_data:
            output_file = os.path.join(output_subdirectory, f"{base_filename}_{chunk_number}.mat")
            sio.savemat(output_file, chunk_data)
            print(f"最後のチャンク {chunk_number} を保存しました: {output_file}")
            print(f"チャンクサイズ: {current_chunk_size / (1024 * 1024):.2f} MB")

        end_time = time.time()
        total_time = end_time - start_time

        print("\n分割が完了しました。")
        print(f"合計処理時間: {total_time:.2f}秒")
        print(f"入力ファイルの合計サイズ: {total_size / (1024 * 1024):.2f} MB")
        print(f"作成されたチャンク数: {chunk_number}")
        print(f"出力ディレクトリ: {output_subdirectory}")

        # 元のファイルを削除
        os.remove(input_mat_file)
        print(f"元のファイル {input_mat_file} を削除しました。")

    @staticmethod
    def merge_mat_files(input_directory, output_file):
        start_time = time.time()

        if not os.path.exists(input_directory):
            raise FileNotFoundError(f"入力ディレクトリ {input_directory} が見つかりません。")

        chunk_files = sorted([f for f in os.listdir(input_directory) if f.endswith(".mat") and MatDevider.is_mat_file(os.path.join(input_directory, f))])

        if not chunk_files:
            raise ValueError(f"ディレクトリ {input_directory} に有効なMATチャンクファイルが見つかりません。")

        merged_data = {}
        total_size = 0

        for chunk_file in chunk_files:
            chunk_path = os.path.join(input_directory, chunk_file)
            chunk_data = sio.loadmat(chunk_path)
            chunk_size = os.path.getsize(chunk_path)
            total_size += chunk_size

            for key, value in chunk_data.items():
                if not key.startswith('__'):
                    if key in merged_data:
                        print(f"警告: 変数 '{key}' が複数のチャンクに存在します。最後のチャンクの値で上書きします。")
                    merged_data[key] = value

            print(f"チャンク {chunk_file} を処理しました。サイズ: {chunk_size / (1024 * 1024):.2f} MB")

        sio.savemat(output_file, merged_data)
        end_time = time.time()
        total_time = end_time - start_time

        print(f"\nマージされたデータを {output_file} に保存しました。")
        print(f"合計処理時間: {total_time:.2f}秒")
        print(f"処理されたチャンクの合計サイズ: {total_size / (1024 * 1024):.2f} MB")
        print(f"処理されたチャンク数: {len(chunk_files)}")

# 使用例
input_mat_file = "/Users/kawabuchy/Public/MATLAB/SUN_OFDM(ver2.0.0)/results/mode_1_mcs_0_ch_1_speed_0_ntr_0_syncMis_1_100_ebn0S_-10_ebn0E_20_nloop_150000_max_noe_400000_min_loop_1500_20240811_163534.mat"
output_directory = "/Users/kawabuchy/Public/MATLAB/SUN_OFDM(ver2.0.0)/results"

# MATファイルの分割
MatDevider.split_mat_file(input_mat_file, output_directory, chunk_size_mb=500)

# MATファイルの結合
base_filename = os.path.splitext(os.path.basename(input_mat_file))[0]
merge_input_directory = os.path.join(output_directory, base_filename)
output_file = os.path.join(output_directory, f"{base_filename}.mat")
MatDevider.merge_mat_files(merge_input_directory, output_file)