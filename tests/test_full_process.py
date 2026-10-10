import unittest
from src.full_process import *


class TestProcessFolder(unittest.TestCase):
    def test_process_folder_valid_directory(self):
        process_folder('C:/helo',print)