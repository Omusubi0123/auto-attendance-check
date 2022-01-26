"""
コアとなる部分のメインプログラム
コマンドラインツールとして使用できるように主要な関数群をまとめて使用できるようにしてある
"""
# 標準ライブラリ
from enum import Enum, auto
from datetime import datetime

# 外部ライブラリ
import fire
import cv2

# このプロジェクトで作成したライブラリ
import core
import core.analysis
import core.change_crontab
from core.export import ClassMatesRegister


class SaveImage(Enum):
    """
    撮影した画像の保存先を指定するenum
    Commands.take_photo()の引数

    Attributes
    ----------
    GUI
        GUIclientからこの引数付きでコマンドが呼ばれた場合、撮影した画像をGUIclientに送信できるような状態を作る
        撮影した最新の画像を特定の場所に保存しておき、GUIからいつでも取り出せるようにしておく
    LOCAL
        撮影した画像をローカルフォルダに保存する
    """

    GUI = auto()
    LOCAL = auto()


class ExportDataType(Enum):
    """
    出欠状況をエクスポートするときに選択可能なファイルのタイプ

    Attributes
    ----------
    CSV
        csvの出欠状況ファイルを選択
    JSON
        jsonの出欠状況ファイルを選択
    """

    CSV = auto()
    JSON = auto()


class Commands(object):
    """
    auto-attendance-checkのAPI
    sshでCLI実行する目的

    Note
    ----
    GUIの操作に対応させて必要なコマンドを作っていく
    """

    def take_photo(
        save_image: SaveImage = SaveImage.LOCAL, save_path: str = "~/aac/Photos"
    ):
        """
        写真を撮影

        Parameters
        ----------
        save_image : SaveImage
            画像の保存先指定する

        save_path : str
            画像を保存するパスを指定する
        """
        img = core.analysis.take_photo()
        if save_image == SaveImage.LOCAL:
            cv2.imwrite(
                f"{save_path}/{datetime.now().strftime(r'%Y-%m-%d%a-%H:%M')}.jpg", img
            )
        elif save_image == SaveImage.GUI:
            cv2.imwrite(f"{save_path}/outgui.jpg", img)

    def analysis():
        """
        撮影した画像の解析を行う
        """
        # res = face_detection(img)
        pass

    def sent_attend_date(data_type: ExportDataType):
        """
        この関数が実行された時点での最新出欠状況をGUIclientにSSHで送信する
        引数でjson,csvを選択する

        Note
        ----
        使用非推奨
        """
        regi = ClassMatesRegister(number_of_students=0)
        if data_type == ExportDataType.CSV:
            regi.exprot_csv()
        elif data_type == ExportDataType.JSON:
            regi.export_json()

    def update_crontab():
        """
        google calendar からこの関数が実行されたときの日にちの時間割を取得し、crontabを変更する
        """
        core.change_crontab.update_schedule()


def main():
    fire.Fire(Commands)
