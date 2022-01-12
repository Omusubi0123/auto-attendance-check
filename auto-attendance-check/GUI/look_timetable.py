# 作成した時間割を見る

import tkinter as tk
import glob
import os
import toml
import timetable_frame


class LookTimetable(tk.Frame):
    """
    mainframeの「時間割」 -> subframeの「時間割を見る」
    ボタンが押された時に作成するフレーム
    """

    def __init__(self, new_window: tk.Toplevel):
        super().__init__(new_window, width=754, height=1080)

        self.toplevel = new_window

        # 時間割フォルダ内のファイル情報を取得する
        path_list, name_list, num = self.file_search("./class_table")

        self.titlelabel = tk.Label(self, text="クリックした時間割を表示します")
        self.titlelabel.place(x=300, y=30)

        self.name_text = []
        self.name_label = []
        self.selectbox = []

        print(num)
        for i in range(0, num):
            print(i)
            self.name_text.append(tk.StringVar(self))
            self.name_text[i].set(name_list[i])
            self.name_label.append(
                tk.Label(self, textvariable=self.name_text[i], font=("Times", 14))
            )

            if i == 0:
                self.selectbox.append(
                    tk.Button(
                        self,
                        text="表示",
                        command=lambda: self.look_table(self.name_text[0].get()),
                    )
                )
            elif i == 1:
                self.selectbox.append(
                    tk.Button(
                        self,
                        text="表示",
                        command=lambda: self.look_table(self.name_text[1].get()),
                    )
                )
            elif i == 2:
                self.selectbox.append(
                    tk.Button(
                        self,
                        text="表示",
                        command=lambda: self.look_table(self.name_text[2].get()),
                    )
                )
            elif i == 3:
                self.selectbox.append(
                    tk.Button(
                        self,
                        text="表示",
                        command=lambda: self.look_table(self.name_text[3].get()),
                    )
                )

            self.name_label[i].place(x=150, y=(120 + (100 * i)))
            self.selectbox[i].place(x=300, y=(120 + (100 * i)))


        self.finish_button = tk.Button(
            self,
            text="終了",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=new_window.destroy,
        )
        self.finish_button.place(x=600, y=900)

        self.grid(row=0, column=0, sticky="nsew")

    def file_search(self, dir: str):
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
            name, ext = os.path.splitext(file)
            name_list.append(name)
            print(str(i) + i)

        return path_list, name_list, num

    def look_table(self, tablename: str) -> bool:
        """
        時間割を表示(編集)する
        """

        edit_frame = timetable_frame.TimetableFrame(self.toplevel)

        # 指定された時間割の内容を取得
        try:
            with open(
                "./class_table/" + tablename + ".toml", "rt", encoding="UTF-8"
            ) as fp:
                data = toml.load(fp)
        except FileNotFoundError as e:
            print(e)
            return False

        text_name = data["table_name"]

        edit_frame.name_text.insert(0, text_name)

        for i in range(0, int(data["class_num"])):
            time = data[str(i+1) + "限目開始"]
            start_time = time.split()
            edit_frame.start_hour[i].set(start_time[0])
            edit_frame.start_min[i].set(start_time[1])

            time = data[str(i+1) + "限目終了"]
            end_time = time.split()
            edit_frame.end_hour[i].set(end_time[0])
            edit_frame.end_min[i].set(end_time[1])

        return True