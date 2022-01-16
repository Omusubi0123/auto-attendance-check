# maniplation.py > SetTimetable() により呼び出されるフレーム

import tkinter as tk
from tkinter import messagebox
import toml


class SubjectFrame(tk.Frame):
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
        self.complete_button.place(x=600, y=520)

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
        self.cancel_button.place(x=460, y=520)

        self.title_label = tk.Label(
            self, text="時間割の設定 科目名を入力してください", font=("Arial", 14)
        )
        self.title_label.place(x=50, y=30)

        self.day_label = []
        self.day_list = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
        self.class_label = []
        self.class_number = ["1限目", "2限目", "3限目", "4限目", "5限目", "6限目", "7限目", "8限目"]

        self.day_name = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        for i in range(0, 7):
            self.day_label.append(
                tk.Label(self, text=self.day_list[i], font=("Times", 14))
            )
            self.day_label[i].place(x=(100 + (i * 90)), y=70)

        for i in range(0, 8):
            self.class_label.append(
                tk.Label(self, text=self.class_number[i], font=("Times", 14))
            )
            self.class_label[i].place(x=30, y=(120 + (50 * i)))

        try:
            with open("./subjects/subjects.toml", "rt", encoding="UTF-8") as fp:
                self.data = toml.load(fp)
        except FileNotFoundError:
            self.data = {}

        # subjects.tomlファイルが存在しない場合
        if not self.data:
            for i in range(0, 7):
                dict_list = {}
                for j in range(0, 8):
                    dict_list[f"class{(j+1)}"] = ""
                self.data[self.day_name[i]] = dict_list

        self.subject = []

        for i in range(0, 7):
            self.subject.append([])
            for j in range(0, 8):
                self.subject[i].append(tk.Entry(self, width=12, font=("Times", 10)))
                try:
                    self.subject[i][j].insert(
                        0, self.data[self.day_name[i]][f"class{(j+1)}"]
                    )
                except KeyError:
                    self.subject[i][j].insert(0, "")
                self.subject[i][j].place(x=(100 + i * 90), y=(124 + (50 * j)))

        self.grid(row=0, column=0, sticky="nsew")

    def completed(self):

        # 時間割変更の確認
        ret = messagebox.askyesno("確認", "この内容で時間割を変更しますか？")
        if ret is False:
            return

        # 最大時間数を計算
        self.class_max = 0
        for i in range(0,7):
            j = 0
            while (str(self.subject[i][j].get()) != "") and (j < 8):
                j += 1
            if j > self.class_max:
                self.class_max = j

        self.write_toml = {}
        self.toml_list = {}
        for i in range(0, 7):
            self.toml_list = {}
            for j in range(0, self.class_max):
                self.toml_list[f"class{(j+1)}"] = str(self.subject[i][j].get())
            self.write_toml[self.day_name[i]] = self.toml_list

        toml.dump(
            self.write_toml,
            open(
                "./subjects/subjects.toml",
                mode="w",
                encoding="UTF-8",
            ),
        )

        messagebox.showinfo("成功", "時間割の作成に成功しました")

        self.toplevel.destroy()
