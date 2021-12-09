#Use under Python3.8
import tkinter as tk
from tkinter import Canvas, ttk
from pathlib import Path
from tkinter.constants import BOTH, E, FLAT, GROOVE, LEFT, NE, NW, RAISED, RIDGE, RIGHT, SE, SOLID, SW, TOP, W, X, Y
from maniplation import Maniplation

#Add tkdesigner to path

#Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# set up main window
window = tk.Tk()
window.title('MANIPLATION')
window.geometry("815x950")
#window.geometry("2000x2000")

# set up main frame
frame = ttk.Frame(window)
frame.pack(fill = tk.BOTH)

# make widgets
background = tk.PhotoImage(file="AI.png")
canvas = tk.Canvas(
    window,
    width=754,
    height=1080,
    scrollregion=(0, 0, 1080, 1260)
)

frame_canvas = tk.Frame(canvas, background='#999999')
canvas.create_window((0,0), window=frame_canvas, anchor=tk.NW)
canvas.create_image(377, 540, image=background)
canvas.pack()
#canvas.grid(row=0, column=0)

# 水平方向のスクロールバーを作成
xbar = tk.Scrollbar(
    frame,
    orient=tk.HORIZONTAL
)

# 垂直方向のスクロールバーを作成
ybar = tk.Scrollbar(
    frame,
    orient=tk.VERTICAL
)

# キャンバスの下に水平方向のスクロールバーを配置
xbar.pack(
    anchor=NW,
    fill=X,
    side=tk.BOTTOM
)

# キャンバスの右に垂直方向のスクロールバーを配置
ybar.pack(
    anchor=NE,
    fill=Y,
    side=tk.RIGHT
)


# スクロールバーのスライダーが動かされた時の処理
xbar.config(command=canvas.xview)
ybar.config(command=canvas.yview)

# スクロールバーをCanvasに関連付け
canvas.config(xscrollcommand=xbar.set)
canvas.config(yscrollcommand=ybar.set)


# Canvasの位置の初期化
canvas.yview_moveto(0)
canvas.xview_moveto(0)

RefAttendData_button = tk.Button(
    frame,
    text="出席状況",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=Maniplation.RefAttendData
)

TakePhotoCom_button = tk.Button(
    frame,
    text="教室撮影",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=Maniplation.TakePhotoCom
)

SetTimetable_button = tk.Button(
    frame,
    text="時間割",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=Maniplation.SetTimetable
)

Configuration_button = tk.Button(
    frame,
    text="設定",
    borderwidth=10,
    padx=40,
    pady=15,
    width=12,
    height=2,
    relief=RAISED,
    cursor="hand2",
    command=Maniplation.Configuration
)

# set widgets
RefAttendData_button.pack(padx=5, pady=10, side=tk.LEFT)
TakePhotoCom_button.pack(padx=5, pady=10, side=tk.LEFT)
SetTimetable_button.pack(padx=5, pady=10, side=tk.LEFT)
Configuration_button.pack(padx=5, pady=10, side=tk.LEFT)

# show main window
if __name__ == "__main__":
    window.mainloop()
