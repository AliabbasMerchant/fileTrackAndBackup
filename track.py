#! /usr/bin/python3
from help import *
import constants

# dict[file_name] = (type, size, full_path, time, stat)
# dict[dir_name] = (type, size, full_path, time, stat, dict)

no_of_files = 0
no_of_dirs = 0
# examine_name = ''
track_number = 0
examine_name = ''
save_filename = ''
data = dict()
_base_path = None
_ignore = False


def get_save_config(base_path: str) -> None:
    global track_number, examine_name, save_filename, data
    examine_name = base_path.strip().split('/')[-1].split('.')[0]  # just in case its a file
    save_filename = examine_name + '.json'
    if os.path.lexists(constants.save_folder_name):
        if os.path.lexists(constants.save_folder_name + "/" + save_filename):
            data = read_from_json_file(constants.save_folder_name + "/" + save_filename)
            track_number = (max([int(x) for x in data.keys()])) + 1
    else:
        execute_bash("mkdir " + constants.save_folder_name)


def get_info_dict(sub_path: str) -> dict:
    global no_of_files, no_of_dirs, _base_path, _ignore
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
        # elif entity == constants.save_folder_name:
        #     ignore_it = True
        if not ignore_it:
            stats = os.stat(full_path + '/' + entity)
            if os.path.isdir(full_path + '/' + entity):
                no_of_dirs += 1
                new_sub_path = sub_path + '/' + entity
                dir_dict = get_info_dict(new_sub_path)
                edit_dict[entity] = {'type': 'dir', 'size': get_size(dir_dict), 'path': full_path + '/' + entity,
                                     'edit_time': get_time(stats), 'stats': stats, 'dirs': dir_dict}
            if os.path.isfile(full_path + '/' + entity):
                no_of_files += 1
                edit_dict[entity] = {'type': 'file', 'size': stats.st_size, 'path': full_path + '/' + entity,
                                     'edit_time': int(get_time(stats)), 'stats': stats}
    return edit_dict


def track(base_path: str, output: bool=False, ignore: bool=False) -> None:
    global _base_path, no_of_dirs, no_of_files, save_filename, data, track_number, _ignore
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
        info = {'type': 'dir', 'size': size, 'path': base_path, 'edit_time': int(get_time(stats)), 'stats': stats,
                'dirs': info}
        write = {'name': examine_name, 'timestamp': time.time(), 'info': info}
        data[track_number] = write
        write_to_json_file(data, constants.save_folder_name + "/" + save_filename)
        if output:
            print("Successfully analysed the folder")
            print("Found {} folder(s)".format(no_of_dirs))
            print("Found {} file(s)".format(no_of_files))
            print("The directory is of size {} kB".format(size / 1000))
            print("A detailed report can be found in " + constants.save_folder_name + "/" + save_filename)
    else:
        no_of_files += 1
        stats = os.stat(base_path)
        info = {'type': 'file', 'size': stats.st_size, 'path': base_path, 'edit_time': int(get_time(stats)),
                'stats': stats}
        write = {'name': examine_name, 'timestamp': time.time(), 'info': info}
        data[track_number] = write
        write_to_json_file(data, constants.save_folder_name + "/" + save_filename)
        if output:
            print("Successfully analysed the file")
            print("The file is of size {} kB".format(stats.st_size / 1000))
            print("A detailed report can be found in " + constants.save_folder_name + "/" + save_filename)
    # pp(info)


if __name__ == '__main__':
    track(os.getcwd(), output=True)