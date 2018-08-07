import json
import os
import subprocess
import time
import constants
import re


def execute_bash(command: str) -> (str, str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if not output is None:
        output = output.decode('ascii')
    if not error is None:
        error = error.decode('ascii')
    return output, error


def get_time(file_info: os.stat_result) -> float:
    return max(file_info.st_atime, file_info.st_ctime, file_info.st_mtime)


def get_size(dir_dict: dict) -> int:
    size = 0
    for key in dir_dict:
        size += dir_dict[key]['size']
    return size


def to_gmt(timestamp: float, convert: bool=True) -> float:
    if convert:
        return timestamp


def to_local_time(timestamp: float, convert: bool=True) -> float:
    if convert:
        return timestamp


def write_to_json_file(dictionary: dict, filename: str) -> None:
    os.open(filename, os.O_CREAT)
    with open(filename, 'w+') as outfile:
        json.dump(dictionary, outfile, indent=2)


def read_from_json_file(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def get_ignore_list():
    with open("{}/{}/{}".format(constants.base_path, constants.save_folder_name, constants.ignore_file), 'r') as f:
        for line in f:
            constants.ignore_regex_list.append(line)
    print(constants.ignore_regex_list)


def display_help() -> None:
    # TODO
    pass


def to_be_ignored(source: str) -> bool:
    source = source.replace('////', '/')  # safe-side
    source = source.replace('///', '/')  # safe-side
    source = source.replace('//', '/')  # safe-side
    for regex in constants.ignore_regex_list:
        if re.search(regex, source):
            return True
    return False
