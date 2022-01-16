# google calendarにタイムテーブルを設定

import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
from tkinter import messagebox
import glob
import os
import google_calendar


class DateFrame(tk.Frame):
    """
    mainframeの「時間割」 -> subframeの「時間割の新規登録」
    ボタンが押された時に作成するフレーム
    """

    def __init__(self, new_window: tk.Toplevel):
        super().__init__(new_window, width=754, height=680)

        self.toplevel = new_window

        self.name_list, self.num = self.file_search("./class_table")
        if self.num == 0:
            messagebox.ERROR("エラー", "タイムテーブルが設定されていません\n「時間割」>「時間割の新規登録」にて作成してください")
            self.toplevel.destroy()
            return

        self.complete_button = tk.Button(
            self,
            text="登録",
            borderwidth=10,
            padx=15,
            pady=5,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.entry,
        )
        self.complete_button.place(x=600, y=500)

        self.cancel_button = tk.Button(
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
        self.cancel_button.place(x=460, y=500)

        # このフレームの説明
        self.title_label = tk.Label(
            self,
            text="選択した日付に選択したタイムテーブルを設定します",
            font=("bold", 14),
        )
        self.title_label.place(x=170, y=30)

        self.explanation_label = tk.Label(
            self,
            text="※選択できるタイムテーブルは1つです\n",
            font=("Arial", 10),
            anchor=tk.W,
        )
        self.explanation_label.place(x=250, y=70)

        # カレンダーの作成・配置
        self.calendar_date = Calendar(self)
        self.calendar_date.place(x=240, y=150)

        # 選択するタイムテーブルのコンボボックスを作成
        self.timetable = ttk.Combobox(
            self, height=10, width=20, values=self.name_list, font=("Times", 14)
        )
        self.timetable.place(x=240, y=350)

        self.grid(row=0, column=0, sticky="nsew")

    def file_search(self, dir: str):
        """
        引数に指定したディレクトリ配下のファイルを探す関数

        return:
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

        return name_list, num

    def entry(self):
        # date = 'mm-dd-yy'
        date = self.calendar_date.get_date()
        date_list = date.split("/")

        # dateをint型のリスト[yyyy, mm, dd]に変換
        register_date = []
        register_date.append(2000 + int(date_list[2]))
        register_date.append(int(date_list[0]))
        register_date.append(int(date_list[1]))

        table_name = self.timetable.get()
        if not table_name:
            messagebox.showerror("エラー", "タイムテーブルを指定してください")
            return

        # 指定した日に既にタイムテーブルが登録されているかチェック
        events = google_calendar.read(1000)
        if events:
            for i in range(0, 3):
                if int(date_list[i]) < 10:
                    date_list[i] = f"0{date_list[i]}"

            check_date = f"20{date_list[2]}-{date_list[0]}-{date_list[1]}"
            i = 0
            # 取得したイベントについて
            for event in events:
                i = 0
                # イベントの開始時刻をstartに格納
                start = event["start"].get("dateTime", event["start"].get("date"))
                # イベントが今日の場合
                if start == check_date:
                    # イベント名を持つタイムテーブルが存在するか判定
                    while (i < self.num) and (event["summary"] != self.name_list[i]):
                        i += 1
                    # イベント名とタイムテーブル名が一致しなかった場合
                    if i < self.num:
                        break

            # タイムテーブル名と一致するその日のイベントが見つからなかった場合
            try:
                if (start == check_date) and (event["summary"] == self.name_list[i]):
                    messagebox.showerror("エラー", "その日は既にタイムテーブルが登録されています")
                    return
            except KeyError:
                # タイトルなしのイベントの場合は無視して登録
                pass

        try:
            google_calendar.entry(register_date, table_name)
        except Exception:
            messagebox.showerror("エラー", "カレンダーに登録できませんでした")
            return

        messagebox.showinfo("成功", "登録に成功しました")
        return
