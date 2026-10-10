from pathlib import Path
from src.file_process_srt import process_srt
from src.full_process import process_folder
from src.gui import Window

# TODO - let the user either choose:
# 1. a file
# 2. multiple files
# 3. a folder
# TODO - make it work with .ass files
# TODO - make a tkinter GUI

def main() -> None:
    window = Window()     


if __name__ == '__main__':
    main()