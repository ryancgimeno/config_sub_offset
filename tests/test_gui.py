import unittest
from pathlib import Path
from src.gui import Window


class WindowTest(unittest.TestCase):
    def test_folder_path(self):
        w = Window()
        w._folder_path = Path('C:\\coding')
        self.assertEqual(w.folder_path, w._folder_path)