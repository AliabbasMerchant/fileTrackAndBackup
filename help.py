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


def cp(source: str, destination: str) -> (str, str):
    source = source.replace("//", "/")
    destination = destination.replace("//", "/")
    # if ' ' in source:
    #     source = '"' + source + '"'
    # if ' ' in destination:
    #     destination = '"' + destination + '"'
    # execute_bash("cp -r -p {} {}".format(source, destination))
    command_list = ["cp", "-r", "-p", source, destination]
    process = subprocess.Popen(command_list, stdout=subprocess.PIPE)
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


def write_to_json_file(dictionary: dict, filename: str) -> None:
    with open(filename, 'w') as outfile:
        json.dump(dictionary, outfile, indent=2)


def read_from_json_file(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def get_ignore_list() -> None:
    with open("{}/{}".format(constants.file_tb_path, constants.ignore_file), 'r') as f:
        for line in f:
            constants.ignore_regex_list.append(line.strip())


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
    source = source.replace('//', '/')
    for pattern in constants.ignore_regex_list:
        if re.search(pattern, source):
            return True
    return False
