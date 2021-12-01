"""
データのエクスポートを行うモジュール
"""

from enum import Enum
import csv
import json
from typing import List


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
        self.data = [
            {
                "student number": students_number,
                "name": "",
                "attendance states": [AttendanceState.NONE.value],
            }
            for students_number in range(1, number_of_students + 1)
        ]

    def insert_data(self, datas: List[AttendanceState]) -> None:
        """
        出欠データの挿入を行う

        Parameters
        ----------
        datas: List[AttendanceState]
            各学生の出席データ
        """
        if len(self.data) != len(datas):
            raise ValueError
        for origin, new in zip(self.data, datas):
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
            for parson in self.data:
                writer.writerows(parson)

    def export_json(self) -> None:
        """
        json形式でデータをエクスポートする

        Notes
        -----
        書き出すファイルのエンコードはutf-8
        """
        with open(f"{self.file_path}.json", mode="w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

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
            for parson in self.data:
                writer.writerows(parson)
