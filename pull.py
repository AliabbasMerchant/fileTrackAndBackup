from help import *
from track import track

_source_path = ''
_destination_path = ''
_ignore = False
source_structure = dict()
destination_structure = dict()
errors = []


def copy(source: str, destination: str):
    global errors
    # both are absolute paths
    # destination is always a directory
    # source may be file/directory
    if not os.path.islink(source):
        if _ignore:
            if not to_be_ignored(source):
                if os.path.isfile(source):
                    # print(source,destination)  # Test
                    op, err = execute_bash("cp -r -p {} {}".format(source, destination))
                    if err is not None:
                        errors.append(err)
                else:
                    new_dir = destination + '/' + source.strip('/').split('/')[-1]
                    try:
                        _ = source.index(constants.save_folder_name)
                    except ValueError:  # copy only if it is not the "save_folder_name" folder
                        execute_bash("mkdir '{}'".format(new_dir))
                        for element in os.listdir(source):
                            copy(source + '/' + element, new_dir)
        else:
            try:
                _ = source.index(constants.save_folder_name)
            except ValueError:  # copy only if it is not the "save_folder_name" folder
                # print(source, destination)  # Test
                op, err = execute_bash("cp -r -p {} {}".format(source, destination))
                if err is not None:
                    errors.append(err)


def back_up_dir(source_dict: dict, destination_dict: dict):
    # {'t': 'd', 's': size, 'p': base_path, 'time': get_time(stats),'dirs': info}
    # {'t': 'f', 's': stats.st_size, 'p': full_path + '/' + entity, 'time': get_time(stats)}
    for entity in source_dict['dirs']:
        if entity in destination_dict['dirs']:
            if source_dict['dirs'][entity]['time'] > destination_dict['dirs'][entity]['time']:
                if not os.path.islink(source_dict['dirs'][entity]['p']):
                    if os.path.isfile(source_dict['dirs'][entity]['p']):
                        copy(source_dict['dirs'][entity]['p'], destination_dict['p'])
                    else:
                        back_up_dir(source_dict['dirs'][entity], destination_dict['dirs'][entity])
        else:
            copy(source_dict['dirs'][entity]['p'], destination_dict['p'])


def pull(source_path: str, destination_path: str, track_first: bool = True, ignore: bool = False) -> list:
    # source_path is a file or directory
    # destination_path is a directory
    global _source_path, _destination_path, source_structure, destination_structure, _ignore, errors
    print("Starting Backup! Please don't turn off your computer till the process finishes.")
    _source_path = source_path
    _destination_path = destination_path
    _ignore = ignore
    if _ignore:
        get_ignore_list()
    source_json_name = source_path.strip().split('/')[-1] + '.json'
    destination_json_name = destination_path.strip().split('/')[-1] + '.json'
    source_dir_path = source_path
    if os.path.isfile(source_dir_path):
        source_dir_path = source_dir_path[0: source_dir_path.rindex('/')]
    if track_first or (not os.path.lexists(source_dir_path + '/' + constants.save_folder_name + '/' + source_json_name)):
        os.chdir(source_dir_path)
        track(source_path, source_dir_path, output=False)
        print("Tracked source")
        os.chdir(destination_path)
    track(destination_path, destination_path, output=False)
    print("Tracked destination")
    source_structure = read_from_json_file(source_dir_path + '/' + constants.save_folder_name + '/' + source_json_name)
    source_structure = source_structure['i']
    destination_structure = read_from_json_file(destination_path +
                                                '/' + constants.save_folder_name + '/' + destination_json_name)
    destination_structure = destination_structure['i']

    if os.path.isfile(source_path):
        destination_structure = destination_structure['dirs']
        edit_time = source_structure['time']
        filename = source_path.strip().split('/')[-1]
        if filename in destination_structure.keys():
            if edit_time > destination_structure[filename]['time']:
                copy(source_path, destination_path)
        else:
            copy(source_path, destination_path)
    else:
        dest_name = destination_path.strip().split('/')[-1]
        source_name = source_path.strip().strip('/').split('/')[-1]
        if dest_name == source_name:
            back_up_dir(source_structure, destination_structure)
        elif source_name in destination_structure['dirs']:
            back_up_dir(source_structure, destination_structure['dirs'][source_name])
        else:
            copy(source_path, destination_path)
    track(destination_path, destination_path, output=True)
    print("All file(s) have been backed-up successfully")
    return errors


if __name__ == '__main__':  # only for testing
    from pprint import pprint as pp
    file_name = os.getcwd().split('/')[-1] + '.json'
    _data = read_from_json_file(os.getcwd() + '/' + constants.save_folder_name + '/' + file_name)
    pp(_data)
