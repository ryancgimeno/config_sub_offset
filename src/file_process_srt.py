import fileinput
from pathlib import Path


# srt format:
# 0         1         2
# 01234567890123456789012345678
# 00:01:23,792 --> 00:01:29,798

def process_srt(file: Path, offset: int, *, start: int = None, stop: int = None) -> None:
    """
    Adjusts the timing of an .srt file given a path and an offset in milliseconds. The user can specify the line to
    start and or stop.
    """
    # Toggles line range mode if 'start' and 'stop'are given as inputs
    if start is not None and stop is not None:
        line_range_mode = True
    else:
        line_range_mode = False

    offset_list = _initialize_offset(offset)
    with fileinput.FileInput(file, inplace = True, encoding = 'utf-8') as f:
        if not line_range_mode:
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

        elif line_range_mode:
            in_line_range = False
            
            for line in f:
                try:
                    if start <= int(line) <= stop:
                        in_line_range = True
                    else:
                        in_line_range = False
                except Exception:
                    pass

                if in_line_range:
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
                        print(line, end = '')
                
                elif not in_line_range:
                    print(line, end = '')



def _split_line(line: str) -> list[str]:
    """
    Splits a string into a list of substrings using space as the delimiter
    """
    return line.split()


def _split_time(formatted_time: str) -> list[int]:
    """
    Takes an .srt formatted time (XX:XX:XX,XXX) and
    converts each unit of time into a list of integers
    """
    hours = int(formatted_time[:2])
    minutes = int(formatted_time[3:5])
    seconds = int(formatted_time[6:8])
    milliseconds = int(formatted_time[9:12])

    return [hours, minutes, seconds, milliseconds]


def _initialize_offset(offset: int) -> list[int]:
    """
    Takes offset in milliseconds and converts it to [hours, minutes, seconds, milliseconds]
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
    """
    'Carries over' in addition if any of the values are above what they are supposed to be. For example, 
    if the adjusted amount of seconds is 62, it will increase minutes by 1 and update seconds to 2
    """
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


def _change_offset_negative(time_list: list[int], offset_list: list[int]) -> list[int]:
    """
    Same as _change_offset but if the offset is negative
    """
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
    """
    Adds leading zeroes to the new time when necessary
    """
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
    """
    Combines the components of a line into a single string
    """
    return first_time + ' --> ' + second_time


