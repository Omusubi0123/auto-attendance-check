# google calendar から今日の時間割を取得し、crontabを変更

"""
毎日午前0時になったらこのファイルを実行する
"""

import google_calendar
import datetime
import glob
import os
from typing import List, Tuple


def file_search(dir: str) -> Tuple[List[str], int]:
    """
    引数に指定したディレクトリ配下のファイルを探す関数

    return:
        path_list: パス名のリスト
        name_list: (拡張子なしの)ファイル名のリスト
        num: ファイル数
    """
    # 指定dir内のすべてのファイルを取得
    path_list = glob.glob(dir + "/*")

    # パスリストからファイル名を抽出
    num = len(path_list)
    name_list = []
    for i in path_list:
        file = os.path.basename(i)
        name, _ext = os.path.splitext(file)
        name_list.append(name)
        print(str(i) + i)

    return name_list, num


def update_schedule() -> bool:
    """
    google calendar から今日の時間割を取得し、crontabを変更する
    """
    events = google_calendar.read()

    if not events:
        return False

    today = datetime.datetime.utcnow().strftime("%F")
    name_list, num = file_search("./photo_table")

    i = 0
    # 直近10件のイベントについて
    for event in events:
        i = 0
        # イベントの開始時刻をstartに格納
        start = event["start"].get("dateTime", event["start"].get("date"))
        # イベントが今日の場合
        if start in today:
            # イベント名を持つタイムテーブルが存在するか判定
            while (i < num) and (event["summary"] != name_list[i]):
                i += 1
            # イベント名とタイムテーブル名が一致しなかった場合
            if i < num:
                break

    # タイムテーブル名と一致する今日のイベントが見つからなかった場合
    if event["summary"] != name_list[i]:
        # crontab内の記述を消す
        os.system("crontab /home/pi/core/photo_table/empty.txt")
        return False

    # 見つかった場合はcrontabを書き換える
    os.system("crontab /home/pi/core/photo_table/" + event["summary"] + ".txt")

    return True
