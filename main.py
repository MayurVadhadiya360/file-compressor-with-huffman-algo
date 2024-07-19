from compressor_ui import GUI, on_closing_window
from tkinter import Tk

if __name__ == '__main__':
    root = Tk()
    compressor = GUI(root)
    root.protocol("WM_DELETE_WINDOW", on_closing_window)
    root.mainloop()
    print('ehllo')