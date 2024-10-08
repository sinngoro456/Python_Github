import sys
import functions
import LINEyahoo.honban.serve as serve

# 日付の最大値をあらかじめ設定
max_day = 1000


# メイン関数
def main(lines):
    output = ""
    input_list = []
    for i in range(len(lines)):
        input_list.append([])
        input_list[i] = lines[i].split(" ")
    num_table = int(input_list[0][0])
    num_time = int(input_list[2][1])
    max_table = input_list[1]
    table_list = []
    for i in range(num_table):
        table = Table(i + 1, input_list[1][1])

    # list_reserve[rev_day][rev_num_time][rev_table]:予約の確認ができるリストを作成[予約番号,人数,指定券or自由権]
    list_reserve = []
    for i in range(max_day):
        list_reserve.append([])
        for j in range(num_time):
            list_reserve[i].append([])
            for k in range(num_table):
                list_reserve[i][j].append(["", "", ""])

    # list_starttime:変わり目の時刻をリストに
    list_starttime = []
    for i in range(num_time):
        temp = input_list[2][2 + i].split("-")
        list_starttime.append(temp[0])

    # 入力の行ごとにクエリを処理
    for i in range(len(input_list) - 3):
        # 時間クエリか判定
        if input_list[i + 3][2] == "time":
            output = serve.time_query(
                output, input_list, list_reserve, list_starttime, num_table, i
            )

        # 指定券発行クエリか判定
        elif input_list[i + 3][2] == "issue-specified":
            result = serve.specified_query(
                output, input_list, list_reserve, list_starttime, i, max_table
            )
            output = result[0]
            list_reserve = result[1]
        # 自由券発行クエリか判定
        elif input_list[i + 3][2] == "issue-unspecified":
            result = serve.unspecified_query(
                output, input_list, list_reserve, list_starttime, i, max_table
            )
            output = result[0]
            list_reserve = result[1]
        # キャンセルクエリか判定
        elif input_list[i + 3][2] == "cancel":
            result = serve.cancel_query(
                output,
                input_list,
                list_reserve,
                list_starttime,
                i,
                max_table,
                num_table,
            )
            output = result[0]
            list_reserve = result[1]

    # outputの冒頭に入る改行を削除して出力
    print(functions.remove_initial_newline(output))


if __name__ == "__main__":
    lines = [
        "3",
        "2 6 8",
        "09:00-15:00 2 09:00-12:00 12:00-15:00",
        "1 09:00 time 1",
        "1 09:10 issue-specified 00001 2 2 1 2",
        "1 09:20 issue-unspecified 00002 2 2 6",
        "1 09:30 cancel 00001",
        "1 12:00 time 2",
        "1 15:00 time 3",
        "2 09:00 time 1",
        "2 12:00 time 2",
    ]
    main(lines)
