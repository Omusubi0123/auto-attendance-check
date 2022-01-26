# maniplation.py > send_tables() により呼び出されるフレーム

import tkinter as tk
from tkinter import messagebox
import paramiko
import glob
import toml
import os


class SendFrame(tk.Frame):
    """
    mainframeの「時間割」 -> subframeの「時間割の新規登録」
    ボタンが押された時に作成するフレーム
    """

    def __init__(self, new_window: tk.Toplevel):
        super().__init__(new_window, width=754, height=680)

        self.toplevel = new_window
        self.timed = 0

        self.complete_button = tk.Button(
            self,
            text="送信",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.transmit,
        )
        self.complete_button.place(x=600, y=500)

        self.cancel_button = tk.Button(
            self,
            text="キャンセル",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=new_window.destroy,
        )
        self.cancel_button.place(x=460, y=500)

        self.title_label = tk.Label(
            self,
            text="ラズパイへ送信したいフォルダを選択してください",
            font=("Arial", 14),
        )
        self.title_label.place(x=170, y=30)

        self.explanation_label = tk.Label(
            self,
            text="class_table : タイムテーブル（授業開始終了時刻）\n"
            + "photo_table : ラズパイ自動撮影用ファイル\n"
            + "subjects : 授業時間割（科目）\n",
            font=("Arial", 10),
            anchor=tk.W,
        )
        self.explanation_label.place(x=250, y=70)

        self.folder1 = "class_table"
        self.folder2 = "photo_table"
        self.folder3 = "subjects"

        self.check_value_class = tk.BooleanVar()
        self.check_value_photo = tk.BooleanVar()
        self.check_value_subjects = tk.BooleanVar()

        self.class_table_check = tk.Checkbutton(
            self, text=self.folder1, var=self.check_value_class, font=("Arial", 14)
        )
        self.photo_table_check = tk.Checkbutton(
            self, text=self.folder2, var=self.check_value_photo, font=("Arial", 14)
        )
        self.subjects_check = tk.Checkbutton(
            self, text=self.folder3, var=self.check_value_subjects, font=("Arial", 14)
        )

        self.class_table_check.place(x=300, y=150)
        self.photo_table_check.place(x=300, y=200)
        self.subjects_check.place(x=300, y=250)

        self.grid(row=0, column=0, sticky="nsew")

    def transmit(self):
        """
        チェックリストにチェックされたフォルダ内のファイルを全てラズパイに送信する
        """

        # チェックボックスの値を読み込む
        check1 = self.check_value_class.get()
        check2 = self.check_value_photo.get()
        check3 = self.check_value_subjects.get()

        if check1 or check2 or check3:

            # raspberrypiのファイルのパスワードファイルの読み込み
            with open("raspberrypi_key.toml", mode="rt", encoding="UTF-8") as fp:
                data = toml.load(fp)

            # SSHでラズパイに接続
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)

            try:
                client.connect(
                    data["IP_ADDRESS"],
                    username=data["USER_NAME"],
                    password=data["PASS_WORD"],
                    timeout=3.9,
                )
            except Exception:
                messagebox.showerror("エラー", "ラズパイに接続できませんでした")
                self.toplevel.destroy()
                return

            # フォルダ内のファイルを転送
            if self.check_value_class.get():
                name_list = self.file_search(f"./{self.folder1}")
                try:
                    sftp_connection = client.open_sftp()
                    for filename in name_list:
                        sftp_connection.put(
                            f"./{self.folder1}/{filename}.toml",
                            f"/home/pi/.config/aac/{self.folder1}/{filename}.toml",
                        )
                except Exception:
                    messagebox.showerror("エラー", f"{self.folder1}の送信に失敗しました")
                    self.toplevel.destroy()
                    return
            if self.check_value_photo.get():
                name_list = self.file_search(f"./{self.folder2}")
                try:
                    sftp_connection = client.open_sftp()
                    for filename in name_list:
                        sftp_connection.put(
                            f"./{self.folder2}/{filename}.toml",
                            f"/home/pi/.config/aac/{self.folder2}/{filename}.toml",
                        )
                except Exception:
                    messagebox.showerror("エラー", f"{self.folder1}の送信に失敗しました")
                    self.toplevel.destroy()
                    return
            if self.check_value_subjects.get():
                name_list = self.file_search(f"./{self.folder3}")
                try:
                    sftp_connection = client.open_sftp()
                    for filename in name_list:
                        sftp_connection.put(
                            f"./{self.folder3}/{filename}.toml",
                            f"/home/pi/.config/aac/{self.folder3}/{filename}.toml",
                        )
                except Exception:
                    messagebox.showerror("エラー", f"{self.folder1}の送信に失敗しました")
                    self.toplevel.destroy()
                    return

            client.close()
            messagebox.showinfo("成功", "送信に成功しました")

        self.toplevel.destroy()
        return

    def file_search(self, dir: str) -> list:
        """
        引数に指定したディレクトリ配下のファイルを探す関数

        return:
            name_list: (拡張子なしの)ファイル名のリスト
        """
        # 指定dir内のすべてのファイルを取得
        path_list = glob.glob(f"{dir}/*")

        # パスリストからファイル名を抽出
        name_list = []
        for i in path_list:
            file = os.path.basename(i)
            name, _ext = os.path.splitext(file)
            name_list.append(name)

        return name_list
