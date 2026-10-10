from pathlib import Path
from src.file_process_srt import process_srt
from src.file_process_ass import process_ass


class FileProcessError(Exception):
    """
    Custom exception for the process_folder function if processing fails
    """
    def __init__(self, message: str, file):
        self.message = message
        self.file = file

    def __str__(self) -> str:
        return f"Selected file '{self.file}' was unable to be processed"


def process_folder(directory: str, offset: int):
    """
    Adjusts the timing of all subtitle files in a given directory by the specified offset
    """
    p = Path(directory)

    if not p.exists():
        raise FileNotFoundError

    for file in p.iterdir():
        if file.suffix == '.srt':
            process_srt(file, offset)
        elif file.suffix == '.ass':
            process_ass(file)
        else:
            raise FileProcessError('Selected file was unable to be processed', file)
