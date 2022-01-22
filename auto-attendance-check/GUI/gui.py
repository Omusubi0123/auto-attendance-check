# GUI main file
# Use under Python3.8
import tkinter as tk
from tkinter.constants import (NE, NW, RAISED, X, Y,)
import maniplation
import sub_frame
import owner

class main_frame:
    def __init__(self):
        # main window の作成
        self.window = tk.Tk()
        self.window.title("MANIPLATION")
        self.window.geometry("815x680")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        """ main frame 作成部 """

        # main frame の作成
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # app frameの作成
        self.frame_app = tk.Frame(self.frame)
        self.frame_app.pack(fill=tk.BOTH)


        # Canvas の作成
        self.background = tk.PhotoImage(file="AI.png")
        self.canvas = tk.Canvas(self.frame, width=754, height=1080, scrollregion=(0, 0, 1080, 1260))

        # Canvas上に配置するframeの作成
        self.frame_canvas = tk.Frame(self.canvas, background="#000000")
        self.canvas.create_window((0, 0), window=self.frame_canvas, anchor=tk.NW)
        self.canvas.create_image(377, 540, image=self.background)


        # 水平方向のスクロールバーを作成
        self.xbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)

        # 垂直方向のスクロールバーを作成
        self.ybar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # キャンバスの下に水平方向のスクロールバーを配置
        self.xbar.pack(anchor=NW, fill=X, side=tk.BOTTOM)

        # キャンバスの右に垂直方向のスクロールバーを配置
        self.ybar.pack(anchor=NE, fill=Y, side=tk.RIGHT)

        # canvasの配置
        self.canvas.pack()

        # スクロールバーのスライダーが動かされた時の処理
        self.xbar.config(command=self.canvas.xview)
        self.ybar.config(command=self.canvas.yview)

        # スクロールバーをCanvasに関連付け
        self.canvas.config(xscrollcommand=self.xbar.set)
        self.canvas.config(yscrollcommand=self.ybar.set)

        # Canvasの位置の初期化
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)

        # buttonの作成と設置
        self.reference_attend_data_button = tk.Button(
            self.frame_app,
            text="出席状況",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=RAISED,
            cursor="hand2",
            command=maniplation.reference_attend_data,
        )
        self.reference_attend_data_button.pack(padx=5, pady=10, side=tk.LEFT)

        # buttonの作成と設置
        self.take_photo_command_button = tk.Button(
            self.frame_app,
            text="教室撮影",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=RAISED,
            cursor="hand2",
            command=lambda: maniplation.take_photo_command(self.background),
        )
        self.take_photo_command_button.pack(padx=5, pady=10, side=tk.LEFT)

        # buttonの作成と設置
        self.timetable_button = tk.Button(
            self.frame_app,
            text="時間割",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=RAISED,
            cursor="hand2",
            command=lambda: sub_frame.SubFrame(self.window, self.frame),
        )
        self.timetable_button.pack(padx=5, pady=10, side=tk.LEFT)

        # buttonの作成と設置
        self.configuration_button = tk.Button(
            self.frame_app,
            text="設定",
            borderwidth=10,
            padx=40,
            pady=15,
            width=12,
            height=2,
            relief=RAISED,
            cursor="hand2",
            command=lambda: maniplation.configuration(self.my_configuration),
        )
        self.configuration_button.pack(padx=5, pady=10, side=tk.LEFT)

        # frame_timetable 作成部
        sub_frame.SubFrame(self.window, self.frame)

        # 個人用設定クラス作成
        self.my_configuration = owner.Owner()

        # frameを前面にする
        self.frame.tkraise()

        self.window.mainloop()

# show main window
if __name__ == "__main__":
    main_frame()
