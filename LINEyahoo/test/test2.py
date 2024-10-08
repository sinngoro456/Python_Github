import sys
import functions

max_day = 1000


def time_to_minutes(time_str):
    # 時間と分の部分を取得
    hours, minutes = map(int, time_str.split(":"))
    # 分単位に変換して合算
    total_minutes = hours * 60 + minutes
    return total_minutes


def time_to_num_time(time_str, list_starttime):
    time_min = time_to_minutes(time_str)
    num_time = 0
    for i in range(len(list_starttime)):
        starttime_min = time_to_minutes(list_starttime[i])
        if time_min >= starttime_min:
            num_time = i + 1
    return num_time


def sort_and_index(text_list):
    # リスト内の文字列を整数に変換して抽出し、整数のリストに格納します
    integers = [int(num) for num in text_list if num.isdigit()]
    # 整数のリストをソートし、その要素番号のリストを作成します
    sorted_indices = sorted(range(len(integers)), key=lambda i: integers[i])
    return sorted_indices


def remove_initial_newline(text):
    if text.startswith("\n"):
        return text.lstrip("\n")
    return text


def main(lines):
    output = ""
    input_list = []
    for i in range(len(lines)):
        input_list.append([])
        input_list[i] = lines[i].split(" ")
    num_table = int(input_list[0][0])
    num_time = int(input_list[2][1])
    max_table = input_list[1]

    # list_reserve[rev_day][rev_num_time][rev_table]で予約の確認ができるリストを作成
    list_reserve = []
    for i in range(max_day):
        list_reserve.append([])
        for j in range(num_time):
            list_reserve[i].append([])
            for k in range(num_table):
                list_reserve[i][j].append("")

    # 入力の行ごとにクエリを処理
    now_day = input_list[3][0]
    now_time = input_list[3][1]
    now_num_time = input_list[3][3]

    # 変わり目の時刻をリストに
    list_starttime = []
    for i in range(num_time):
        temp = input_list[2][2 + i].split("-")
        list_starttime.append(temp[0])

    for i in range(len(input_list) - 3):
        # 時間クエリか判定
        if input_list[i + 3][2] == "time":

            now_day = input_list[i + 3][0]
            now_time = input_list[i + 3][1]
            now_num_time = int(input_list[i + 3][3])
            for num_time in range(len(list_starttime)):
                if list_starttime[num_time] == now_time:
                    for i_table in range(num_table):
                        rev_num = list_reserve[int(now_day) - 1][int(now_num_time) - 1][
                            int(i_table)
                        ]
                        if rev_num != "":
                            output = (
                                output
                                + "\n"
                                + now_day
                                + " "
                                + now_time
                                + " table "
                                + str(i_table + 1)
                                + " = "
                                + rev_num
                            )

        # 指定券発行クエリか判定
        elif input_list[i + 3][2] == "issue-specified":
            now_day = input_list[i + 3][0]
            now_time = input_list[i + 3][1]
            now_num_time = functions.time_to_num_time(now_time, list_starttime)
            rev_num = input_list[i + 3][3]
            rev_day = input_list[i + 3][4]
            rev_num_time = input_list[i + 3][5]
            rev_num_people = input_list[i + 3][6]
            rev_table = input_list[i + 3][7]
            if now_day == rev_day and now_num_time == rev_num_time:
                output = (
                    output
                    + "\n"
                    + now_day
                    + " "
                    + now_time
                    + " Error: the current slot cannot be specified."
                )
            elif (int(now_day) > int(rev_day)) or (
                int(now_day) == int(rev_day) and int(now_num_time) > int(rev_num_time)
            ):
                output = (
                    output
                    + "\n"
                    + now_day
                    + " "
                    + now_time
                    + " Error: a past time cannot be specified."
                )
            elif int(rev_num_people) > int(max_table[int(rev_table) - 1]):
                output = (
                    output
                    + "\n"
                    + now_day
                    + " "
                    + now_time
                    + " Error: the maximum number of people at the table has been exceeded."
                )
            elif (
                list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                    int(rev_table) - 1
                ]
                != ""
            ):
                output = (
                    output
                    + "\n"
                    + now_day
                    + " "
                    + now_time
                    + " Error: the table is occupied."
                )
            else:
                list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                    int(rev_table) - 1
                ] = rev_num
                output = output + "\n" + now_day + " " + now_time + " " + rev_num
        # 自由券発行クエリか判定
        elif input_list[i + 3][2] == "issue-unspecified":
            now_day = input_list[i + 3][0]
            now_time = input_list[i + 3][1]
            now_num_time = functions.time_to_num_time(now_time, list_starttime)
            rev_num = input_list[i + 3][3]
            rev_day = input_list[i + 3][4]
            rev_num_time = input_list[i + 3][5]
            rev_num_people = input_list[i + 3][6]
            sort_table_list = functions.sort_and_index(max_table)
            can_rev = False
            for i_table in sort_table_list:
                if not (now_day == rev_day and now_num_time == rev_num_time):
                    if not (
                        (int(now_day) > int(rev_day))
                        or (
                            int(now_day) == int(rev_day)
                            and int(now_num_time) > int(rev_num_time)
                        )
                    ):
                        if int(rev_num_people) <= int(max_table[i_table]):
                            if (
                                list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                                    int(i_table)
                                ]
                                == ""
                            ):
                                list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                                    int(i_table)
                                ] = rev_num
                                output = (
                                    output
                                    + "\n"
                                    + now_day
                                    + " "
                                    + now_time
                                    + " "
                                    + rev_num
                                    + " "
                                    + str(i_table + 1)
                                )
                                can_rev = True
                                break
            if not can_rev:
                output = (
                    output
                    + "\n"
                    + now_day
                    + " "
                    + now_time
                    + " Error: no available table is found."
                )
        # キャンセルクエリか判定
        elif input_list[i + 3][2] == "cancel":
            now_day = input_list[i + 3][0]
            now_time = input_list[i + 3][1]
            now_num_time = functions.time_to_num_time(now_time, list_starttime)
            rev_num = input_list[i + 3][3]
            can_cancel = False
            for j in range(i):
                if input_list[j + 3][3] == input_list[i + 3][3]:
                    if (int(input_list[j + 3][4]) + 1 > int(now_day)) or (
                        int(input_list[j + 3][4]) + 1 == int(now_day)
                        and now_num_time < int(input_list[j + 3][5])
                    ):
                        output = (
                            output
                            + "\n"
                            + now_day
                            + " "
                            + now_time
                            + " Canceled "
                            + rev_num
                        )
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            int(rev_table)
                        ] = ""
                        can_cancel = True
                        break
            if not can_cancel:
                output = (
                    output
                    + "\n"
                    + now_day
                    + " "
                    + now_time
                    + " Error: no reserved table is found."
                )
    print(functions.remove_initial_newline(output))


if __name__ == "__main__":
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip("\r\n"))
    main(lines)
