import os
import scipy.io as sio
import shutil


class MatDevider:
    @staticmethod
    def is_mat_file(file_path):
        """ファイルがMATファイルかどうかを判定する"""
        try:
            sio.loadmat(file_path, verify_compressed_data_integrity=False)
            return True
        except Exception as e:
            print(f"MATファイルの読み込み中にエラーが発生しました: {e}")
            return False

    @staticmethod
    def split_mat_file(input_mat_file, chunk_size=500):
        if not os.path.exists(input_mat_file):
            raise FileNotFoundError(f"入力ファイル {input_mat_file} が見つかりません。")

        if not MatDevider.is_mat_file(input_mat_file):
            raise ValueError(
                f"入力ファイル {input_mat_file} はMATファイルではありません。"
            )

        base_filename = os.path.splitext(os.path.basename(input_mat_file))[0]
        output_directory = os.path.dirname(input_mat_file)
        output_subdirectory = os.path.join(output_directory, base_filename) + "_dv"

        # 出力ディレクトリが存在しない場合は作成
        if not os.path.exists(output_subdirectory):
            os.makedirs(output_subdirectory)

        print(f"ファイル {input_mat_file} の読み込みを開始します...")
        mat_data = sio.loadmat(input_mat_file)

        chunk_size_bytes = chunk_size
        var_names = [key for key in mat_data.keys() if not key.startswith("__")]

        chunk_data = {}
        current_chunk_size = 0
        chunk_number = 1
        total_size = 0

        for var_name in var_names:
            var_data = mat_data[var_name]
            var_size = var_data.nbytes

            # 変数が100MBを超える場合、さらに分割
            if var_size > chunk_size_bytes:
                num_chunks = (var_size // chunk_size_bytes) + 1
                for i in range(num_chunks):
                    start_index = i * chunk_size_bytes // var_data.itemsize
                    end_index = (i + 1) * chunk_size_bytes // var_data.itemsize
                    chunk_data[var_name] = var_data[start_index:end_index]

                    output_file = os.path.join(
                        output_subdirectory, f"{var_name}_{i + 1}.mat"
                    )
                    sio.savemat(output_file, chunk_data)
                    print(
                        f"変数 '{var_name}' のチャンク {i + 1} を保存しました: {output_file}"
                    )
                    print(f"チャンクサイズ: {chunk_size:.2f}")

                    chunk_data = {}
            else:
                # 既存のチャンク処理
                chunk_data[var_name] = var_data
                current_chunk_size += var_size

                if current_chunk_size >= chunk_size_bytes:
                    output_file = os.path.join(
                        output_subdirectory, f"{base_filename}_{chunk_number}.mat"
                    )
                    sio.savemat(output_file, chunk_data)
                    print(f"チャンク {chunk_number} を保存しました: {output_file}")
                    print(
                        f"チャンクサイズ: {current_chunk_size / (1024 * 1024):.2f} MB"
                    )

                    chunk_data = {}
                    current_chunk_size = 0
                    chunk_number += 1

        if chunk_data:
            output_file = os.path.join(output_subdirectory, f"{chunk_number}.mat")
            sio.savemat(output_file, chunk_data)
            print(f"最後のチャンク {chunk_number} を保存しました: {output_file}")
            print(f"チャンクサイズ: {current_chunk_size / (1024 * 1024):.2f} MB")

        print("\n分割が完了しました。")
        print(f"入力ファイルの合計サイズ: {total_size / (1024 * 1024):.2f} MB")
        print(f"作成されたチャンク数: {chunk_number}")
        print(f"出力ディレクトリ: {output_subdirectory}")

        # 元のファイルを削除
        os.remove(input_mat_file)
        print(f"元のファイル {input_mat_file} を削除しました。")
        return output_subdirectory

    @staticmethod
    def merge_mat_files(input_directory):

        if not os.path.exists(input_directory):
            raise FileNotFoundError(
                f"入力ディレクトリ {input_directory} が見つかりません。"
            )

        chunk_files = sorted(
            [
                f
                for f in os.listdir(input_directory)
                if f.endswith(".mat")
                and MatDevider.is_mat_file(os.path.join(input_directory, f))
            ]
        )

        if not chunk_files:
            raise ValueError(
                f"ディレクトリ {input_directory} に有効なMATチャンクファイルが見つかりません。"
            )

        merged_data = {}
        total_size = 0

        for chunk_file in chunk_files:
            chunk_path = os.path.join(input_directory, chunk_file)
            chunk_data = sio.loadmat(chunk_path)
            chunk_size = os.path.getsize(chunk_path)
            total_size += chunk_size

            for key, value in chunk_data.items():
                if not key.startswith("__"):
                    if key in merged_data:
                        print(
                            f"警告: 変数 '{key}' が複数のチャンクに存在します。最後のチャンクの値で上書きします。"
                        )
                    merged_data[key] = value

            print(
                f"チャンク {chunk_file} を処理しました。サイズ: {chunk_size / (1024 * 1024):.2f} MB"
            )

        output_file = os.path.join(
            os.path.dirname(input_directory),  # 入力ディレクトリの親ディレクトリを取得
            os.path.basename(input_directory).replace("_dv", "")
            + ".mat",  # "_dv"を省いて.matを追加
        )

        sio.savemat(output_file, merged_data)
        # 元のファイルを削除
        shutil.rmtree(input_directory)

        print(f"\nマージされたデータを {output_file} に保存しました。")
        print(f"処理されたチャンクの合計サイズ: {total_size:.2f}")
        print(f"処理されたチャンク数: {len(chunk_files)}")
        return output_file


# 使用
input_mat_file = r"C:\prog\Github_test\PC1\results\SUN_OFDM(ver2.0.0)\mode_3_mcs_-2_ch_6_SNRflag_SNR (dB)_speed_1_ntr_0_syncMis_1_100_ebn0S_-16_ebn0E_8_nloop_1_max_noe_1000_min_loop_0_20241017_193947.mat"

# MATファイルの分割
output_subdirectory = MatDevider.split_mat_file(input_mat_file, chunk_size=10)
mat_file = MatDevider.merge_mat_files(output_subdirectory)
