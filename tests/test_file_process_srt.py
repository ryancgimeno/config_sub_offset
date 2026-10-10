import unittest
import src.file_process_srt as file_process_srt


class TestPrivateFunctions(unittest.TestCase):
    def test_split_line(self):
        line = '00:01:23,792 --> 00:01:29,798'
        self.assertEqual(file_process_srt._split_line(line), ['00:01:23,792', '-->', '00:01:29,798'])

    def test_split_time(self):
        line = '05:21:23,792 --> 05:21:29,798'
        one_split_time = file_process_srt._split_line(line)[0]
        self.assertEqual(file_process_srt._split_time(one_split_time), [5, 21, 23, 792])

    def test_initialize_offset(self):
        offset_list = [3, 25, 45, 678]
        self.assertEqual(file_process_srt._initialize_offset(12345678), offset_list)

    def test_change_offset(self):
        list1 = [1, 2, 3, 4]
        list2 = [3, 5, 7, 9]
        expected_list = [4, 7, 10, 13]
        self.assertEqual(file_process_srt._change_offset(list1, list2), expected_list)

    def test_change_offset_overflow(self):
        original_time = [40, 50, 50, 500]
        offset_time = [1, 15, 15, 550]
        expected_list = [42, 6, 6, 50]
        self.assertEqual(file_process_srt._change_offset(original_time, offset_time), expected_list)

    # reformat tests
    def test_reformat_time_all_numbers_filled(self):
        self.assertEqual(file_process_srt._reformat_time([11, 11, 11, 111]), '11:11:11,111')

    def test_reformat_time_all_numbers_zero(self):
        self.assertEqual(file_process_srt._reformat_time([0, 0, 0, 0]), '00:00:00,000')

    def test_reformat_time_all_one_digit_numbers(self):
        self.assertEqual(file_process_srt._reformat_time([1, 1, 1, 1]), '01:01:01,001')

    def test_reformat_time_milliseconds_two_digit_number(self):
        self.assertEqual(file_process_srt._reformat_time([0, 0, 0, 25]), '00:00:00,025')


    def test_reformat_line(self):
        self.assertEqual(file_process_srt._reformat_line('00:00:00,025', '01:01:01,001'),
                         '00:00:00,025 --> 01:01:01,001')
