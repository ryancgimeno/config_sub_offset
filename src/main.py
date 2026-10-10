from src.file_process_srt import *
from src.full_process import *

OFFSET_PROMPT = 'Offset: '
FOLDER_PROMPT = 'Folder Directory: '

# TODO - make it work with .ass files
# TODO - make a tkinter GUI

def main() -> None:
    offset = int(input(OFFSET_PROMPT))
    folder_path = input(FOLDER_PROMPT)
    process_folder(folder_path, offset)


if __name__ == '__main__':
    main()