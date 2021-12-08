#Use under Python3.8
from tkinter import *
from pathlib import Path

#Add tkdesigner to path

#Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

#make window
window = Tk()
window.title('MANIPLATION')
window.getometry("1000x750")


#show window
window.mainloop()