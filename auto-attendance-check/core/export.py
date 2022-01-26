"""
データのエクスポートを行うモジュール
"""

from enum import Enum
import csv
import json
import toml
import datetime
from typing import Any, Dict, List, MutableMapping, Optional


class AttendanceState(Enum):
    """
    出席の正体を表す列挙体

    Attributs
    ---------
    ABSENCE : str
        欠席
    LATENESS : str
        遅刻
    AUTHORIZEED_ABSENCE : str
        公欠
    ATTEND : str
        出席
    NONE : str
        初期状態、未確認状態
    ERROR : str
        エラー
    """

    ABSENCE = "absence"
    LATENESS = "lateness"
    AUTHORIZEED_ABSENCE = "authorized absence"
    ATTEND = "attend"
    NONE = "none"
    ERROR = "error"


class ClassMatesRegister:
    """
    クラスの出席状況を管理するクラス

    Attributs
    ---------
    file_path : str
        ファイルの書き出しを行うパス
    data : list
        各学生の学生自身の情報、学生の出席状態を持つリスト

    Example
    -------
    file_path = "./attendance_datas/"
    data = [
        {
            "student number": 20,
            "name": "山田一郎",
            "attandance states": [AttendanceState.ATTEND.value]
        },
        {
            "student number": 21,
            "name": "山田二郎",
            "attandance states": [AttendanceState.ABSENCE.value]
        }
    ]
    """

    def __init__(
        self, number_of_students: int, path: str = "./attendance_data"
    ) -> None:
        """
        初期化を行う

        Parameters
        ----------
        number_of_students : int
            クラス当たりの学生数

        path : str
            データのエクスポート先のパス
            拡張子なし
            プログラム実行ポイントからの相対パス

        """
        self.file_path = path
        self.datas: List[Dict[str, Any]] = [
            {
                "student number": students_number,
                "name": "",
                "attendance states": [AttendanceState.NONE.value],
            }
            for students_number in range(1, number_of_students + 1)
        ]

    def update(self, datas: List[bool]) -> None:
        """
        出欠データの更新を行う

        Parameters
        ----------
        datas : List[bool]
            画像を解析した結果のデータ
        """
        for data, new in zip(self.datas, datas):
            top: str = data["attendance states"].pop()
            if top == AttendanceState.NONE.value:
                if new:
                    data["attendance states"].append(AttendanceState.ATTEND.value)
                else:
                    data["attendance states"].append(AttendanceState.LATENESS.value)
            elif top == AttendanceState.LATENESS.value:
                data["attendance states"].append(AttendanceState.LATENESS.value)
            else:
                data["attendance states"].append(top)

    def insert_data(self, datas: List[AttendanceState]) -> None:
        """
        出欠データの挿入を行う
        内部的に使用、プライベート関数

        Parameters
        ----------
        datas: List[AttendanceState]
            各学生の出席データ
        """
        if len(self.datas) != len(datas):
            raise ValueError
        for origin, new in zip(self.datas, datas):
            origin["attendance states"].append(new.value)

    def exprot_csv(self) -> str:
        """
        csv形式でデータをエクスポートする

        Notes
        -----
        書き出すファイルのエンコードはutf-8
        """
        with open(f"{self.file_path}.csv", mode="w", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, ["student number", "name", "attendance state"]
            )
            writer.writeheader()
            for parson in self.datas:
                writer.writerows(parson)

    def export_json(self) -> None:
        """
        json形式でデータをエクスポートする

        Notes
        -----
        書き出すファイルのエンコードはutf-8
        """
        with open(f"{self.file_path}.json", mode="w", encoding="utf-8") as file:
            json.dump(self.datas, file, ensure_ascii=False, indent=4)

    def export_excel_csv(self) -> None:
        """
        excelで読み込み可能な形式のcsvでデータをエクスポートする

        Notes
        -----
        書き出すファイルのエンコードはutf-8
        """
        with open(f"{self.file_path}.csv", mode="w", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                dialect="excel",
            )
            writer.writeheader()
            for parson in self.datas:
                writer.writerows(parson)


def cast_str_to_time(time: str) -> datetime.time:
    """
    crontabの設定ファイルとして使用している時間割データの時間から
    datetime.time型の時間データへ型変換を行う関数

    Parameters
    ----------
    time : str
        crontabの設定ファイルとして使用している時間割データの時間（文字列）

    Return
    ------
        datetime.time型の時間
    """
    hour, min = map(int, time.split())
    return datetime.time(hour, min)


def is_class(nth: int, class_table: MutableMapping[str, Any]) -> bool:
    """
    いまが授業中かどうか判定する関数

    Parameters
    ----------
    nth : int
        何時間目か
        例: n限目ならn
    class_table : MutableMapping[str, Any]
        読み込んだ時間割データ

    Return
    ------
        今がn限目だった場合にtrue、そうでなければfalse
    """
    start: str = f"{nth}限目開始"
    end: str = f"{nth}限目終了"
    start: datetime.time = cast_str_to_time(class_table[start])
    end: datetime.time = cast_str_to_time(class_table[end])

    now = datetime.datetime.now().time()
    if start <= now and now <= end:
        return True
    return False


def get_class_info(class_table_path: str) -> Optional[int]:
    """
    今が何限目の授業中かだどうかデータを返す

    Parameters
    ----------
    class_table_path : str
        時間割データのパス
    
    Return
    ------
        今が授業中であればその授業が何限目かを表す数字
        今が授業中でなければNone
    """
    class_table = toml.load(open(class_table_path))
    class_num: int = class_table["class_num"]
    for nth in range(class_num):
        if is_class(nth, class_table):
            return nth
    return None
