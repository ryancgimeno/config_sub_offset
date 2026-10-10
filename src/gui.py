"""
Defines the Graphical User Interface (GUI) for the subtile offset program using tkinter
"""

import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path

from src.file_process_srt import process_srt
from src.full_process import process_folder


# TODO - the window should NOT do any of the processing, it should just give the information it has
# and then the other modules will handle it

# in other words, do not import any of the modules ive made so far


# the main problem im running into is how do i get the information from the class into the main function?

class Window:
    """
    Graphical interface for the subtitle offset program
    """

    debug = 'Y'  # either is 'Y' or 'N'

    def __init__(self) -> None:
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
        # file_label.pack()

        file_button = tk.Button(self.root,
                                command = self._ask_directory,
                                text = 'Select')
        # file_button.pack()

        # Declares the variable for storing offset and line range
        self._offset = tk.IntVar()
        self._line_range = tk.StringVar()

        # Creates the offset label and entry
        offset_label = tk.Label(self.root,
                                text = 'Set offset amount (ms)')
        # offset_label.pack()

        offset_entry = tk.Entry(self.root,
                                textvariable = self._offset)
        # offset_entry.pack()

        # Creates the line range label and entry
        line_range_label = tk.Label(self.root,
                                    text = '[OPTIONAL] Set Line Range (Format is 7-15, inclusive)')

        line_range_entry = tk.Entry(self.root,
                                    textvariable = self._line_range)


        # Creates the run button
        run_button = tk.Button(self.root,
                               command = self._create_input_dictionary,
                               text = 'Run')

        # If debug mode is on, then there will be a print button
        if self.debug == 'Y':
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
        print(self._input_dict)


    def _ask_directory(self) -> None:
        self._file_path = Path(fd.askdirectory())


    def _create_input_dictionary(self) -> None:
        # the .get() is necessary for offset and line range because they are tkinter TypeVars and not 
        # their actual types

        print(f'Before the conditional, file: {self._file_path}, offset: {self._offset.get()},  line: {self._line_range.get()}')

        if self._file_path and self._offset:
            print('going into the postive in statment')
            self._input_dict = {'file_path': self._file_path,
                                'offset': self._offset.get(),  
                                'line_range': self._line_range.get()}

            process_folder(self._input_dict['file_path'], self._input_dict['offset'])
            
            print('Setting input dictionary after success')

        else:
            # TODO - return an error or like pop up if all the required fields aren't filled in

            print('Unsuccessful')

            self._input_dict = None


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
