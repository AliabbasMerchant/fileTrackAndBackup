#! /usr/bin/python3
from help import *
import time

# short-forms are used, so as to reduce the .json file size
# t : type - d or f
# d : directory
# f : file
# ts : timestamp
# dirs : The dictionary containing info about directory contents
# time : edit time of the file/folder
# s : size of the file/folder
# p : full path of the file/folder
# n : name of the main file/folder in the .json file
# i : info about the contents in the .json file

# folder = {'t': 'd', 's': get_size(dir_dict), 'p': full_path + '/' + entity, 'time': get_time(stats), 'dirs': dir_dict}
# file = {'t': 'f', 's': stats.st_size, 'p': full_path + '/' + entity, 'time': get_time(stats)}

# info = {'t': 'd', 's': size, 'p': base_path, 'time': get_time(stats), 'dirs': info}
# write = {'n': examine_name, 'ts': time.time(), 'i': info}

# info = {'t': 'f', 's': stats.st_size, 'p': base_path, 'time': get_time(stats)}
# write = {'n': examine_name, 'ts': time.time(), 'i': info}

no_of_files = 0
no_of_dirs = 0
examine_name = ''
save_filename = ''
_base_path = None
_ignore = False
errors = []


def get_save_config(base_path: str) -> None:
    global examine_name, save_filename
    examine_name = base_path.strip().split('/')[-1]
    save_filename = examine_name + '.json'
    if not os.path.lexists(constants.save_folder_name):
        execute_bash("mkdir " + constants.save_folder_name)


def get_info_dict(sub_path: str) -> dict:
    global no_of_files, no_of_dirs, _base_path, _ignore, errors
    full_path = _base_path + '/' + sub_path
    full_path = full_path.strip()
    if full_path.endswith('/'):
        full_path = full_path[:-1]
    edit_dict = dict()

    entity_list = os.listdir(full_path)
    for entity in entity_list:
        ignore_it = False
        if _ignore and to_be_ignored(full_path + '/' + entity):  # ignoring cache temp etc files
            ignore_it = True
        if not ignore_it:
            try:
                stats = os.stat(full_path + '/' + entity)
                if not os.path.islink(full_path + '/' + entity):
                    if os.path.isdir(full_path + '/' + entity):
                        no_of_dirs += 1
                        new_sub_path = sub_path + '/' + entity
                        dir_dict = get_info_dict(new_sub_path)
                        edit_dict[entity] = {'t': 'd', 's': get_size(dir_dict), 'p': full_path + '/' + entity,
                                             'time': get_time(stats), 'dirs': dir_dict}
                    if os.path.isfile(full_path + '/' + entity):
                        no_of_files += 1
                        edit_dict[entity] = {'t': 'f', 's': stats.st_size, 'p': full_path + '/' + entity,
                                             'time': get_time(stats)}
            except FileNotFoundError:
                errors.append(full_path + '/' + entity)
    return edit_dict


def track(base_path: str, dir_path: str, output: bool = False, ignore: bool = False) -> list:
    global _base_path, no_of_dirs, no_of_files, save_filename, _ignore, errors
    no_of_dirs = 0
    no_of_files = 0
    print("Tracking...")
    _base_path = base_path
    _ignore = ignore
    get_save_config(base_path)
    if _ignore:
        get_ignore_list()
    if os.path.isdir(base_path):
        info = get_info_dict('')
        size = get_size(info)
        no_of_dirs += 1
        stats = os.stat(base_path)
        info = {'t': 'd', 's': size, 'p': base_path, 'time': get_time(stats), 'dirs': info}
        write = {'n': examine_name, 'ts': time.time(), 'i': info}
        write_to_json_file(write, constants.save_folder_name + "/" + save_filename)
        if output:
            print("Successfully analysed the folder " + base_path)
            print("Found {} folder(s)".format(no_of_dirs))
            print("Found {} file(s)".format(no_of_files))
            print("The directory is of size {}".format(get_size_format(size)))
            print("A detailed report can be found in " +
                  dir_path + "/" + constants.save_folder_name + "/" + save_filename)
    else:
        no_of_files += 1
        stats = os.stat(base_path)
        info = {'t': 'f', 's': stats.st_size, 'p': base_path, 'time': get_time(stats)}
        write = {'n': examine_name, 'ts': time.time(), 'i': info}
        write_to_json_file(write, constants.save_folder_name + "/" + save_filename)
        if output:
            print("Successfully analysed the file")
            print("The file is of size {}".format(get_size_format(stats.st_size)))
            print("A detailed report can be found in " +
                  dir_path + "/" + constants.save_folder_name + "/" + save_filename)
    # pp(info)
    return errors


if __name__ == '__main__':
    track(os.getcwd(), os.getcwd(), output=True)
