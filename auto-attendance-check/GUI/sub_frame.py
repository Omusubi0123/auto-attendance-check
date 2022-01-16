import tkinter as tk
import maniplation as maniplation

""" frame_timetable 作成部 """


def change_main_frame(frame: tk.Frame):
    frame.tkraise()


class SubFrame(tk.Frame):
    def __init__(self, window: tk.Tk, frame: tk.Frame):
        super().__init__(window, width=754, height=680)

        # サブウィンドウのbuttonの作成
        button_change = tk.Button(self, text="メインウィンドウに移動", command=self.destroy)
        button_change.pack()

        set_timetable_button = tk.Button(
            self,
            text="タイムテーブルの新規登録",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=maniplation.set_timetable,
        )

        set_timetable_button.pack(padx=5, pady=10, side=tk.TOP)

        set_calender_button = tk.Button(
            self,
            text="タイムテーブルの指定",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=maniplation.set_calender,
        )
        set_calender_button.pack(padx=5, pady=10, side=tk.TOP)

        look_timetable_button = tk.Button(
            self,
            text="タイムテーブルを見る",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=maniplation.looktimetable,
        )
        look_timetable_button.pack(padx=5, pady=10, side=tk.TOP)

        self.grid(row=0, column=0, sticky="nsew")

        set_subjects_button = tk.Button(
            self,
            text="時間割の登録・編集",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=maniplation.set_subjects,
        )

        set_subjects_button.pack(padx=5, pady=10, side=tk.TOP)

        send_tables_button = tk.Button(
            self,
            text="時間割・タイムテーブルの送信",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=maniplation.send_tables,
        )

        send_tables_button.pack(padx=5, pady=10, side=tk.TOP)
