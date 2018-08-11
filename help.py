import json
import os
import subprocess
import constants
import re


def execute_bash(command: str) -> (str, str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output is not None:
        output = output.decode('ascii')
    if error is not None:
        error = error.decode('ascii')
    return output, error


def get_time(file_info: os.stat_result) -> int:
    return int(max(file_info.st_atime, file_info.st_ctime, file_info.st_mtime))


def get_size(dir_dict: dict) -> int:
    size = 0
    for key in dir_dict:
        size += dir_dict[key]['s']
    return size


# def to_gmt(timestamp: float, convert: bool = True) -> float:
#     if convert:
#         return timestamp


# def to_local_time(timestamp: float, convert: bool = True) -> float:
#     if convert:
#         return timestamp


def write_to_json_file(dictionary: dict, filename: str) -> None:
    # os.open(filename, os.O_CREAT)
    with open(filename, 'w') as outfile:
        json.dump(dictionary, outfile, indent=2)


def read_from_json_file(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def get_ignore_list():
    with open("{}/{}/{}".format(constants.file_tb_path, constants.save_folder_name, constants.ignore_file), 'r') as f:
        for line in f:
            constants.ignore_regex_list.append(line)
    # print(constants.ignore_regex_list)


def display_help() -> None:
    # TODO
    pass


def get_size_format(size: int) -> str:
    if size < 1000:
        return str(size) + ' bytes'
    elif size < 1000000:
        return str(size / (10 ** 3)) + ' kB'
    elif size < 1000000000:
        return str(size / (10 ** 6)) + ' MB'
    else:
        return str(size / (10 ** 9)) + ' GB'


def to_be_ignored(source: str) -> bool:
    source = source.replace('////', '/')  # safe-side
    source = source.replace('///', '/')  # safe-side
    source = source.replace('//', '/')
    for regex in constants.ignore_regex_list:
        if re.search(regex, source):
            return True
    return False
