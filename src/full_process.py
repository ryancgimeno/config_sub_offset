from pathlib import Path

from src.file_process_srt import *
from src.file_process_ass import *

def process_folder(directory: str, offset: int):
    p = Path(directory)

    if not p.exists():
        raise Exception  # placeholder exception

    for file in p.iterdir():
        if file.suffix == '.srt':
            process_srt(file, offset)
        elif file.suffix == '.ass':
            process_ass(file)
        else:
            pass # exception later