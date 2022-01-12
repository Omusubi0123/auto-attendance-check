# GUI sub file

import ssh
import timetable_frame
import look_timetable
import owner
import configuration_frame
import tkinter as tk

# ボタンクリック時の操作


def reference_attend_data():
    """
    「出席状況」button was pushed
    Notes
    powershellを開き、出席データを格納している機器へアクセス

    """
    pass


def take_photo_command():
    """
    「教室撮影」button was pushed

    Notes
        powershellを開き、ラズパイにSSH接続
        →ラズパイへ撮影を命令 撮影した教室の画像を画像処理部の画像フォルダに格納する
        →撮影した画像はPC側にも送信 GUI操作者による確認を可能に
        →ラズパイへ画像解析を命令
        →ラズパイとのSSH接続を終了

    Variable
    --------
    'rpistill -o /home/pi/rpicamera/rpicamera.sh'
    '画像解析部の呼び出し'
    (/home/pi/rpicamera/rpicamera.sh : 画像撮影命令が記述されているファイル)
    """

    # raspberrypiのファイルのパスワードファイルの読み込み
    with open("raspberrypi_key.txt", mode="r") as fp:
        l_strip = [s.strip() for s in fp.readlines()]

    # 呼び出すコマンド
    cmd = 'python core/main.py "TakePhoto"'

    ssh.connect_SSH(
        IP_ADDRESS=l_strip[0], USER_NAME=l_strip[1], PASSWORD=l_strip[2], CMD=cmd
    )


def set_timetable():
    """
    「時間割」button was pushed

    Notes
        新しく時間割を作成する
        「時間割の名前」と「時間割」を新たなウィンドウで入力させ、
        指定したフォーマットでテキストファイルに出力する。
    """

    new_window = tk.Toplevel()
    new_window.geometry("750x600")

    timetable_frame.TimetableFrame(new_window)


def set_calender():
    """
    「カレンダー」button was pushed
    """
    pass


def looktimetable():
    """
    設定した「時間割」を見る
    """
    new_window = tk.Toplevel()
    new_window.geometry("750x680")

    look_timetable.LookTimetable(new_window)


def configuration(mysettings: owner.Owner):
    """
    「設定」button was pushed
    Notes
    """
    new_window = tk.Toplevel()
    new_window.geometry("500x550")

    configuration_frame.ConfigurationFrame(new_window, mysettings)

    pass
