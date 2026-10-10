"""
Defines the Graphical User Interface (GUI) for the subtile offset program using tkinter
"""

import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path

from src.file_process_srt import process_srt
from src.full_process import process_folder


class Window:
    """
    Graphical interface for the subtitle offset program
    """
    def __init__(self) -> None:
        # Initializing attributes
        self._file_path = None
        self._offset = None
        self._line_range = None
        self._input_dict = None

        # Creates the root window
        self.root = tk.Tk()
        self.root.title('Subtitle Offset')
        self.root.geometry('700x800')

        # Sets the logo on the top left
        self.root.iconphoto(False, tk.PhotoImage(file = 'logo.png'))

        # Creates the folder selection label and button
        file_label = tk.Label(self.root,
                              text = 'Select a folder')

        file_button = tk.Button(self.root,
                                command = self._ask_directory,
                                text = 'Select')

        # Declares the variable for storing offset and line range
        self._offset = tk.IntVar()
        self._line_range = tk.StringVar()

        # Creates the offset label and entry
        offset_label = tk.Label(self.root,
                                text = 'Set offset amount (ms)')

        offset_entry = tk.Entry(self.root,
                                textvariable = self._offset)

        # Creates the line range label and entry
        line_range_label = tk.Label(self.root,
                                    text = '[OPTIONAL] Set Line Range (Format is 7-15, inclusive)')

        line_range_entry = tk.Entry(self.root,
                                    textvariable = self._line_range)

        # Creates the run button
        run_button = tk.Button(self.root,
                               command = self._run,
                               text = 'Run')

        # Temporary print button for debugging
        print_button = tk.Button(self.root,
                                 command = self.print_values,
                                 text = 'print')
        print_button.grid(column = 5, row = 6)

        # Sets the grid up
        file_button.grid(column = 0, row = 0)
        file_label.grid(column = 1, row = 0)

        offset_entry.grid(column = 0, row = 1)
        offset_label.grid(column = 1, row = 1)

        line_range_entry.grid(column = 0, row = 2)
        line_range_label.grid(column = 1, row = 2)

        run_button.grid(column = 0, row = 5)

        # Keeps the window running
        self.root.mainloop()


    def print_values(self):
        """
        Debugging function to print the input dictionary
        """
        print(self._input_dict)


    def _ask_directory(self) -> None:
        """
        Asks the user for a directory to choose and saves the Path as a class attribute
        """
        self._file_path = Path(fd.askdirectory())


    def _run(self) -> None:
        """
        Runs the logic of the program
        """
        process_folder(self._file_path, self._offset.get())
            

    def file_path(self) -> Path:
        """
        Returns the user's selected file path
        """
        return self._file_path


    def offset(self) -> int:
        """
        Returns the user provided offset
        """
        return self._offset


    def line_range(self) -> str:
        """
        Returns the user provided line range or None if they left it blank
        """
        return self._line_range


    def input_dictionary(self) -> dict:
        """
        Returns the user's input in a dictionary
        """
        return self._input_dict


if __name__ == '__main__':
    window = Window()
    window.initialize()
