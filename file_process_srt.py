from pathlib import Path
import fileinput

# srt format:
# 0         1         2
# 01234567890123456789012345678
# 00:01:23,792 --> 00:01:29,798


def _split_line(line: str) -> list[str]:
    """
    Splits a string into a list of substrings using space as the delimiter.
    """
    return line.split()


def _split_time(formatted_time: str) -> list[int]:
    """
    Takes an .srt formatted time (XX:XX:XX,XXX) and
    converts each unit of time into a list of integers.
    """
    hours = int(formatted_time[:2])
    minutes = int(formatted_time[3:5])
    seconds = int(formatted_time[6:8])
    milliseconds = int(formatted_time[9:12])

    return [hours, minutes, seconds, milliseconds]


def _initialize_offset(offset: int) -> list[int]:
    """
    Offset is in milliseconds
    """
    if offset < 0:
        offset_negative = True
        offset = -offset
    else:
        offset_negative = False


    offset_hours = int(offset // (3.6 * 10 ** 6))    # I don't think it'll ever get high so no %
    offset_minutes = offset // (6 * 10 ** 4) % 60    # up to 60
    offset_seconds = offset // 1000 %  60    # up to 60
    offset_milliseconds = offset % 1000    # up to 1000

    if offset_negative:
        return [-offset_hours, -offset_minutes, -offset_seconds, -offset_milliseconds]
    else:
        return [offset_hours, offset_minutes, offset_seconds, offset_milliseconds]


def _change_offset(time_list: list[int], offset_list: list[int]) -> list[int]:
    changed_time_list = []
    i = 0
    while i in range(4):
        changed_time_list.append(time_list[i] + offset_list[i])
        i += 1
    if changed_time_list[1] >= 60: # check if minutes >= 60
        changed_time_list[1] %= 60
        changed_time_list[0] += 1

    if changed_time_list[2] >= 60: # check if seconds >= 60
        changed_time_list[2] %= 60
        changed_time_list[1] += 1

    if changed_time_list[3] >= 1000: # check if ms >= 1000
        changed_time_list[3] %= 1000
        changed_time_list[2] += 1

    return changed_time_list

# TODO
def _change_offset_negative(time_list: list[int], offset_list: list[int]) -> list[int]:
    changed_time_list = []
    i = 0
    while i in range(4):
        changed_time_list.append(time_list[i] + offset_list[i])
        i += 1

    if changed_time_list[0] < 0:
        changed_time_list[0] = 0

    if changed_time_list[1] < 0:
        changed_time_list[1] += 60
        changed_time_list[0] -= 1

    if changed_time_list[2] < 0: # check if seconds >= 60
        changed_time_list[2] += 60
        changed_time_list[1] -= 1

    if changed_time_list[3] < 0: # check if ms >= 1000
        changed_time_list[3] += 1000
        changed_time_list[2] -= 1

    return changed_time_list


def _reformat_time(time_list: list[int]):
    str_list = [str(x) for x in time_list]

    i = 0
    while i < 3:
        if int(str_list[i]) // 10 == 0:
            str_list[i] = '0' + str_list[i]
        i += 1

    if int(str_list[3]) // 10 == 0:
        str_list[3] = '00' + str_list[3]

    elif int(str_list[3]) // 10 <= 9:
        str_list[3] = '0' + str_list[3]

    final_string = ':'.join(str_list[:3]) + ',' + str_list[3]
    return final_string


def _reformat_line(first_time: str, second_time: str) -> str:
    return first_time + ' --> ' + second_time


def process_srt(file: Path, offset: int) -> None:
    offset_list = _initialize_offset(offset)
    with fileinput.FileInput(file, inplace = True, encoding = 'utf-8') as f:
        for line in f:
            if '-->' in line:
                srt_split_line = _split_line(line)

                first_time = _split_time(srt_split_line[0])
                second_time = _split_time(srt_split_line[2])

                if offset > 0:

                    new_first_time = _change_offset(first_time, offset_list)
                    new_second_time = _change_offset(second_time, offset_list)
                else:
                    new_first_time = _change_offset_negative(first_time, offset_list)
                    new_second_time = _change_offset_negative(second_time, offset_list)

                new_line = _reformat_line(_reformat_time(new_first_time), _reformat_time(new_second_time))

                print(line.replace(line, new_line))

            else:
                print(line, end='')
