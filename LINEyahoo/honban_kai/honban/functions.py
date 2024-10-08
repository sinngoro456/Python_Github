# 文字列のtimeを大小が比較できるように分の数値に
def time_to_minutes(time_str):
    # 時間と分の部分を取得
    hours, minutes = map(int, time_str.split(":"))
    # 分単位に変換して合算
    total_minutes = hours * 60 + minutes
    return total_minutes


# 文字列のtimeをint型のnum_timeに
def time_to_num_time(time_str, list_starttime):
    time_min = time_to_minutes(time_str)
    num_time = 0
    for i in range(len(list_starttime)):
        starttime_min = time_to_minutes(list_starttime[i])
        if time_min >= starttime_min:
            num_time = i + 1
    return num_time


# 　テーブルの収容人数のリストを人数順にソートするリストを作成
def sort_and_index(text_list):
    # リスト内の文字列を整数に変換して抽出し、整数のリストに格納
    integers = [int(num) for num in text_list if num.isdigit()]
    # 整数のリストをソートし、その要素番号のリストを作成
    sorted_indices = sorted(range(len(integers)), key=lambda i: integers[i])
    return sorted_indices


# outputの冒頭に入る改行を削除
def remove_initial_newline(text):
    if text.startswith("\n"):
        return text.lstrip("\n")
    return text


def sort_list_by_other_list(list1, list2):
    sorted_lists = sorted(zip(list2, list1))
    return [x for _, x in sorted_lists]
