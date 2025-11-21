# main.py
import tkinter as tk
from ui import WordleGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()