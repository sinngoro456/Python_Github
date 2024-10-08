import functions


# 時間クエリの処理
def time_query(output, input_list, list_reserve, list_starttime, num_table, i):
    now_day = input_list[i + 3][0]
    now_time = input_list[i + 3][1]
    now_num_time = int(input_list[i + 3][3])
    for num_time in range(len(list_starttime)):
        if list_starttime[num_time] == now_time:
            for i_table in range(num_table):
                rev_num = list_reserve[int(now_day) - 1][int(now_num_time) - 1][
                    int(i_table)
                ][0]
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
    return output


# 指定券発行クエリの処理
def specified_query(output, input_list, list_reserve, list_starttime, i, max_table):
    now_day = input_list[i + 3][0]
    now_time = input_list[i + 3][1]
    now_num_time = functions.time_to_num_time(now_time, list_starttime)
    rev_num = input_list[i + 3][3]
    rev_day = input_list[i + 3][4]
    rev_num_time = input_list[i + 3][5]
    rev_num_people = input_list[i + 3][6]
    rev_table = input_list[i + 3][7]

    # 発行可否の判定とoutputの作成
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
        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][int(rev_table) - 1][0]
        != ""
    ):
        output = (
            output + "\n" + now_day + " " + now_time + " Error: the table is occupied."
        )
    else:
        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][int(rev_table) - 1][
            0
        ] = rev_num
        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][int(rev_table) - 1][
            1
        ] = rev_num_people
        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][int(rev_table) - 1][
            2
        ] = "specified"
        output = output + "\n" + now_day + " " + now_time + " " + rev_num
    return output, list_reserve


# 自由券発行クエリの処理
def unspecified_query(output, input_list, list_reserve, list_starttime, i, max_table):
    now_day = input_list[i + 3][0]
    now_time = input_list[i + 3][1]
    now_num_time = functions.time_to_num_time(now_time, list_starttime)
    rev_num = input_list[i + 3][3]
    rev_day = input_list[i + 3][4]
    rev_num_time = input_list[i + 3][5]
    rev_num_people = input_list[i + 3][6]
    sort_table_list = functions.sort_and_index(max_table)

    # 発行可否の判定とoutputの作成
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
                        ][0]
                        == ""
                    ):
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            int(i_table)
                        ][0] = rev_num
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            int(i_table)
                        ][1] = rev_num_people
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            int(i_table)
                        ][2] = "unspecified"
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
    return output, list_reserve


# キャンセルクエリの処理
def cancel_query(
    output, input_list, list_reserve, list_starttime, i, max_table, num_table
):
    now_day = input_list[i + 3][0]
    now_time = input_list[i + 3][1]
    now_num_time = functions.time_to_num_time(now_time, list_starttime)
    rev_num = input_list[i + 3][3]

    #  キャンセル対象のrev_dayとrev_num_timeをinputから探索
    for j in range(i):
        if rev_num == input_list[i - j + 2][3]:
            rev_day = input_list[i - j + 2][4]
            rev_num_time = input_list[i - j + 2][5]

    # 当該予約番号の予約があるかどうかを判定
    count_reserve = 0
    count_cancel = 0
    output_list = []
    output_list = functions.remove_initial_newline(output).split("\n")
    for i_day in range(len(output_list)):
        temp = output_list[i_day].split(" ")
        output_list[i_day] = temp
        # 当該予約番号の予約の数をカウント
        if len(output_list[i_day]) >= 3:
            if output_list[i_day][2] == rev_num:
                count_reserve = count_reserve + 1
            # 当該予約番号のキャンセルの数をカウント
            if output_list[i_day][2] == "Canceled":
                if len(output_list[i_day]) >= 4:
                    if output_list[i_day][3] == rev_num:
                        count_cancel = count_cancel + 1

    # キャンセル対象の探索とoutputの作成
    can_cancel = False
    for i_day in range(i):
        if input_list[i_day + 3][3] == input_list[i + 3][3]:
            if (int(input_list[i_day + 3][4]) + 1 > int(now_day)) or (
                int(input_list[i_day + 3][4]) + 1 == int(now_day)
                and now_num_time < int(input_list[i_day + 3][5])
            ):
                # キャンセルが確定 当該箇所のキャンセルと再調整のためキャンセルされたテーブルの
                # 最大人数、テーブル番号を保存
                output = (
                    output + "\n" + now_day + " " + now_time + " Canceled " + rev_num
                )
                for i_table in range(
                    len(list_reserve[int(rev_day) - 1][int(rev_num_time) - 1])
                ):
                    if (
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            0
                        ]
                        == rev_num
                    ):
                        i_cancel_table = (
                            i_table  # キャンセルされたテーブルのテーブル番号を保存
                        )
                        cancel_num_people = max_table[
                            i_table
                        ]  # キャンセルされたテーブルの最大人数を保存
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            0
                        ] = ""
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            1
                        ] = ""
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            2
                        ] = ""
                can_cancel = True

                # キャンセル確定後、予約票の再調整
                num_people_table = []

                # num_table:キャンセルのあった各時間帯の人数を別リストに
                for i_table in range(
                    len(list_reserve[int(rev_day) - 1][int(rev_num_time) - 1])
                ):
                    try:
                        num_people_table.append(
                            int(
                                list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                                    i_table
                                ][1]
                            )
                        )
                    except (ValueError, TypeError) as e:
                        num_people_table.append(0)
                # num_table:キャンセルのあった各時間帯の人数を別リストに

                # unspecified_sort_table:キャンセルのあった各時間帯の自由券の予約席を人数でソートしてリスト化
                temp1 = list(range(0, int(num_table)))
                temp2 = []
                for i_table in range(len(temp1)):
                    if list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                        2
                    ] in ["unspecified"]:
                        temp2.append(temp1[i_table])

                unspecified_sort_table = functions.sort_list_by_other_list(
                    temp2, num_people_table
                )
                # unspecified_sort_table:キャンセルのあった各時間帯の自由券の予約席を人数でソートしてリスト化

                # unspecified_sort_tableをたどりながら、人数の少ない予約席に自由券の予約席を詰めていく
                for i_table in unspecified_sort_table:
                    a = int(
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            1
                        ]
                    )
                    b = int(cancel_num_people)
                    if int(
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            1
                        ]
                    ) <= int(cancel_num_people):
                        cancel_num_people = list_reserve[int(rev_day) - 1][
                            int(rev_num_time) - 1
                        ][i_table][1]
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            i_cancel_table
                        ][0] = list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            i_table
                        ][
                            0
                        ]
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            i_cancel_table
                        ][1] = list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            i_table
                        ][
                            1
                        ]
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            i_cancel_table
                        ][2] = list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][
                            i_table
                        ][
                            2
                        ]

                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            0
                        ] = ""
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            1
                        ] = ""
                        list_reserve[int(rev_day) - 1][int(rev_num_time) - 1][i_table][
                            2
                        ] = ""
                break
    if not can_cancel:
        output = (
            output
            +     "\n"
            + now_day
            + " "
            + now_time
            + " Error: no reserved table is found."
        )
    return output, list_reserve
