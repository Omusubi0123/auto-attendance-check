# maniplation.py > SetTimetable() により呼び出されるフレーム

import tkinter as tk
from tkinter import ttk
import toml
import owner
import ssh


class TimetableFrame(tk.Frame):
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
            text="完了",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.completed,
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

        self.error_text = tk.StringVar(self)
        self.error_label = tk.Label(
            self, textvariable=self.error_text, font=("Times", 14)
        )
        self.error_label.place(x=200, y=30)

        self.name_label = tk.Label(self, text="時間割名(ローマ字)", font=("Times", 14))
        self.name_label.place(x=30, y=70)
        self.name_text = tk.Entry(self, width=20, font=("Timer", 18))
        self.name_text.place(x=240, y=70, height=30)

        self.label_start = []
        self.label_end = []
        self.label_hour = []
        self.label_minutes = []

        self.start_hour = []
        self.start_min = []
        self.end_hour = []
        self.end_min = []

        self.hours = [(h % 24) + 1 for h in range(6, 24 + 6)]
        self.minutes = [m for m in range(0, 60, 5)]
        self.hours.append(None)
        self.minutes.append(None)

        for i in range(0, 7):
            self.start_hour.append(
                ttk.Combobox(
                    self, height=4, width=4, values=self.hours, font=("Times", 14)
                )
            )
            self.start_min.append(
                ttk.Combobox(
                    self, height=4, width=4, values=self.minutes, font=("Times", 14)
                )
            )
            self.end_hour.append(
                ttk.Combobox(
                    self, height=4, width=4, values=self.hours, font=("Times", 14)
                )
            )
            self.end_min.append(
                ttk.Combobox(
                    self, height=4, width=4, values=self.minutes, font=("Times", 14)
                )
            )
            self.label_start.append(
                tk.Label(self, text=(str)(i + 1) + "時間目開始", font=("Times", 14))
            )
            self.label_end.append(
                tk.Label(self, text=(str)(i + 1) + "時間目終了", font=("Times", 14))
            )
            self.label_hour.append(tk.Label(self, text="時", font=("Times", 14)))
            self.label_hour.append(tk.Label(self, text="時", font=("Times", 14)))
            self.label_minutes.append(tk.Label(self, text="分", font=("Times", 14)))
            self.label_minutes.append(tk.Label(self, text="分", font=("Times", 14)))

            self.start_hour[i].place(x=150, y=(120 + (50 * i)))
            self.start_min[i].place(x=250, y=(120 + (50 * i)))
            self.end_hour[i].place(x=490, y=(120 + (50 * i)))
            self.end_min[i].place(x=590, y=(120 + (50 * i)))

            self.label_start[i].place(x=10, y=(120 + (50 * i)))
            self.label_hour[i * 2].place(x=220, y=(120 + (50 * i)))
            self.label_minutes[i * 2].place(x=320, y=(120 + (50 * i)))
            self.label_end[i].place(x=350, y=(120 + (50 * i)))
            self.label_hour[i * 2 + 1].place(x=560, y=(120 + (50 * i)))
            self.label_minutes[i * 2 + 1].place(x=660, y=(120 + (50 * i)))

        self.grid(row=0, column=0, sticky="nsew")

    def completed(self):
        if self.name_text.get() != "":
            self.timed = self.check_logic()
            if self.timed != -1:
                self.error_text.set("")
                self.confirm(self.toplevel)
        else:
            self.error_text.set("時間割名を入力してください")

    def check_logic(self) -> int:
        """
        入力された授業時間割が論理的に正しいか否か判定する関数

        return:
            True -> i(時限数)
            False -> -1
        """
        i = 0
        while i < 7:
            s1 = self.start_hour[i].get()
            s2 = self.start_min[i].get()
            e1 = self.end_hour[i].get()
            e2 = self.end_min[i].get()

            if s1 != "" or s2 != "" or e1 != "" or e2 != "":
                if s1 == "" or s2 == "" or e1 == "" or e2 == "":
                    self.error_text.set("同一授業欄の中に値が指定されていない箇所があります")
                    return -1
                else:
                    s1 = int(s1)
                    s2 = int(s2)
                    e1 = int(e1)
                    e2 = int(e2)
                    if (s1 > e1) or ((s1 == e1) and (s2 > e2)):
                        self.error_text.set("終了時刻が開始時刻よりも早い箇所があります")
                        return -1
                    elif i != 0:
                        pe1 = int(self.end_hour[i - 1].get())
                        pe2 = int(self.end_min[i - 1].get())
                        if (s1 < pe1) or ((s1 == pe1) and (s2 < pe2)):
                            self.error_text.set("開始時刻が前の授業終了時刻より早い箇所があります")
                            return -1
            else:
                return i

            i = i + 1

    def confirm(self, toplevel: tk.Toplevel):
        confirm_frame = tk.Frame(toplevel, width=754, height=1080)

        confirmed_button = tk.Button(
            confirm_frame,
            text="確認",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=lambda: self.make_file(toplevel),
        )
        confirmed_button.place(x=600, y=500)

        modify_button = tk.Button(
            confirm_frame,
            text="修正",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=confirm_frame.destroy,
        )
        modify_button.place(x=460, y=500)

        cancel_button = tk.Button(
            confirm_frame,
            text="キャンセル",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=toplevel.destroy,
        )
        cancel_button.place(x=320, y=500)

        name_label = tk.Label(confirm_frame, text="時間割名", font=("Times", 14))
        name_label.place(x=30, y=70)
        name_text_label = tk.Label(
            confirm_frame, width=20, text=self.name_text.get(), font=("Times", 14)
        )
        name_text_label.place(x=90, y=70)

        label_start = []
        label_end = []
        label_hour = []
        label_minutes = []

        start_hour = []
        start_min = []
        end_hour = []
        end_min = []

        for i in range(0, 7):
            start_hour.append(
                tk.Label(
                    confirm_frame, text=self.start_hour[i].get(), font=("Times", 14)
                )
            )
            start_min.append(
                tk.Label(
                    confirm_frame, text=self.start_min[i].get(), font=("Times", 14)
                )
            )
            end_hour.append(
                tk.Label(confirm_frame, text=self.end_hour[i].get(), font=("Times", 14))
            )
            end_min.append(
                tk.Label(confirm_frame, text=self.end_min[i].get(), font=("Times", 14))
            )

            label_start.append(
                tk.Label(confirm_frame, text=(str)(i + 1) + "時間目開始", font=("Times", 14))
            )
            label_end.append(
                tk.Label(confirm_frame, text=(str)(i + 1) + "時間目終了", font=("Times", 14))
            )
            label_hour.append(tk.Label(confirm_frame, text="時", font=("Times", 14)))
            label_hour.append(tk.Label(confirm_frame, text="時", font=("Times", 14)))
            label_minutes.append(tk.Label(confirm_frame, text="分", font=("Times", 14)))
            label_minutes.append(tk.Label(confirm_frame, text="分", font=("Times", 14)))

            start_hour[i].place(x=150, y=(120 + (50 * i)))
            start_min[i].place(x=250, y=(120 + (50 * i)))
            end_hour[i].place(x=490, y=(120 + (50 * i)))
            end_min[i].place(x=590, y=(120 + (50 * i)))

            label_start[i].place(x=10, y=(120 + (50 * i)))
            label_hour[i * 2].place(x=220, y=(120 + (50 * i)))
            label_minutes[i * 2].place(x=320, y=(120 + (50 * i)))
            label_end[i].place(x=350, y=(120 + (50 * i)))
            label_hour[i * 2 + 1].place(x=560, y=(120 + (50 * i)))
            label_minutes[i * 2 + 1].place(x=660, y=(120 + (50 * i)))

        confirm_frame.grid(row=0, column=0, sticky="nsew")

    def make_file(self, toplevel: tk.Toplevel):
        """
        入力された時間割をフォーマットに従った.tomlファイルとして出力


        ファイル名 : 「時間割名」.toml
        ```toml
        table_name = '時間割名'
        class_num = '時間数'
        "1限目開始" = '開始時間'
        "1限目終了" = '終了時間'
        ......(時間数分記述)
        ```
        """

        # 時間割閲覧用ファイル作成
        write_toml = {}
        write_toml["table_name"] = self.name_text.get()
        write_toml["class_num"] = str(self.timed)

        for i in range(0, self.timed):
            s1 = self.start_hour[i].get()
            s2 = self.start_min[i].get()
            e1 = self.end_hour[i].get()
            e2 = self.end_min[i].get()

            write_toml[str(i + 1) + "限目開始"] = s1 + " " + s2
            write_toml[str(i + 1) + "限目終了"] = e1 + " " + e2

        toml.dump(
            write_toml,
            open(
                "./class_table/" + self.name_text.get() + ".toml",
                mode="w",
                encoding="UTF-8",
            ),
        )

        # ラズパイ撮影用ファイル作成
        setting = owner.Owner()
        interval = setting.interval

        enter = []
        enter.append("# " + self.name_text.get() + " timetable\n")
        for i in range(0, self.timed):
            t1 = int(self.start_hour[i].get())
            t2 = int(self.start_min[i].get())
            e1 = int(self.end_hour[i].get())
            e2 = int(self.end_min[i].get())

            while True:
                enter.append(
                    str(t2) + " " + str(t1) + " * * * /home/pi/core/rpicamera.sh\n"
                )

                t2 += interval
                if t2 >= 60:
                    t1 += 1
                    t2 -= 60

                if t1 > e1 or (t1 == e1 and t2 >= e2):
                    break

            enter.append(
                str(e2) + " " + str(e1) + " * * * /home/pi/core/rpicamera.sh\n"
            )
            enter.append("0 0 * * * python /home/pi/core/change_crontab.py\n")

        with open("./photo_table/" + self.name_text.get() + ".txt", mode="w") as f:
            f.writelines(enter)

        # 作成したファイルをSSHでラズパイに送信
        # raspberrypiのファイルのパスワードファイルの読み込み
        with open("raspberrypi_key.txt", mode="r") as fp:
            l_strip = [s.strip() for s in fp.readlines()]

        # 呼び出すコマンド
        cmd = 'python core/main.py "add_phototable"'

        ssh.connect_SSH(
            IP_ADDRESS=l_strip[0], USER_NAME=l_strip[1], PASSWORD=l_strip[2], CMD=cmd
        )

        toplevel.destroy()
