# GUI main file
# Use under Python3.8
import tkinter as tk

# from tkinter import Canvas, ttk
from pathlib import Path
from tkinter.constants import (
    NE,
    NW,
    RAISED,
    X,
    Y,
)
import maniplation
import sub_frame
import owner

# main window の作成
window = tk.Tk()
window.title("MANIPLATION")
window.geometry("815x680")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

""" main frame 作成部 """

# main frame の作成
frame = tk.Frame(window)
frame.grid(row=0, column=0, sticky="nsew")

# app frameの作成
frame_app = tk.Frame(frame)
frame_app.pack(fill=tk.BOTH)


# Canvas の作成
background = tk.PhotoImage(file="AI.png")
canvas = tk.Canvas(frame, width=754, height=1080, scrollregion=(0, 0, 1080, 1260))

# Canvas上に配置するframeの作成
frame_canvas = tk.Frame(canvas, background="#000000")
canvas.create_window((0, 0), window=frame_canvas, anchor=tk.NW)
canvas.create_image(377, 540, image=background)


# 水平方向のスクロールバーを作成
xbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)

# 垂直方向のスクロールバーを作成
ybar = tk.Scrollbar(frame, orient=tk.VERTICAL)

# キャンバスの下に水平方向のスクロールバーを配置
xbar.pack(anchor=NW, fill=X, side=tk.BOTTOM)

# キャンバスの右に垂直方向のスクロールバーを配置
ybar.pack(anchor=NE, fill=Y, side=tk.RIGHT)

# canvasの配置
canvas.pack()

# スクロールバーのスライダーが動かされた時の処理
xbar.config(command=canvas.xview)
ybar.config(command=canvas.yview)

# スクロールバーをCanvasに関連付け
canvas.config(xscrollcommand=xbar.set)
canvas.config(yscrollcommand=ybar.set)

# Canvasの位置の初期化
canvas.yview_moveto(0)
canvas.xview_moveto(0)

# buttonの作成と設置
reference_attend_data_button = tk.Button(
    frame_app,
    text="出席状況",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=maniplation.reference_attend_data
)
reference_attend_data_button.pack(padx=5, pady=10, side=tk.LEFT)

# buttonの作成と設置
take_photo_command_button = tk.Button(
    frame_app,
    text="教室撮影",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=maniplation.take_photo_command
)
take_photo_command_button.pack(padx=5, pady=10, side=tk.LEFT)

# buttonの作成と設置
timetable_button = tk.Button(
    frame_app,
    text="時間割",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=lambda: sub_frame.SubFrame(window, frame)
    # command=changeSubFrame
)
timetable_button.pack(padx=5, pady=10, side=tk.LEFT)

# buttonの作成と設置
configuration_button = tk.Button(
    frame_app,
    text="設定",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=lambda: maniplation.configuration(my_configuration),
)
configuration_button.pack(padx=5, pady=10, side=tk.LEFT)

# frame_timetable 作成部
sub_frame.SubFrame(window, frame)

# 個人用設定クラス作成
my_configuration = owner.Owner()

# frameを前面にする
frame.tkraise()

# show main window
if __name__ == "__main__":
    window.mainloop()
