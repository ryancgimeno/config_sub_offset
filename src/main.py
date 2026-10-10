from src.gui import Window

# TODO - let the user either choose:
# 1. a file
# 2. multiple files
# 3. a folder
# TODO - make it work with .ass files
# TODO - make a tkinter GUI

'''
OFFSET_PROMPT = 'Offset: '
FOLDER_PROMPT = 'Folder Directory: '

def main() -> None:
    offset = int(input(OFFSET_PROMPT))
    folder_path = input(FOLDER_PROMPT)
    process_folder(folder_path, offset)
'''

def main() -> None:
    window = Window()
    window.initialize()
    while True:
        while not window.input_dictionary():
            pass
        
        input_dict = window.input_dictionary().values()
        file_path = input_dict['file_path']
        offset = input_dict['offset']
        line_range = input_dict['line_range']

        print(input_dict)




if __name__ == '__main__':
    main()