import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path


class Window:
    def __init__(self) -> None:
        self._folder_path = None


    def initialize(self):
        root = tk.Tk()
        root.title('Subtitle Offset')
        root.geometry('700x800')

        file_button = tk.Button(root,
                                command = self._ask_directory,
                                text = 'Select a folder',
                                justify = 'left')
        file_button.pack()

        root.mainloop()


    def folder_path(self) -> Path:
        return self._folder_path


    def _ask_directory(self) -> None:
        folder_path = fd.askdirectory()
        self._folder_path = Path(folder_path)


if __name__ == '__main__':
    window = Window()
    window.initialize()