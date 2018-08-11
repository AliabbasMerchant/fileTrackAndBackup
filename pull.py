from help import *
from track import track

_source_path = ''
_destination_path = ''
_ignore = False
source_structure = dict()
destination_structure = dict()


def copy(source: str, destination: str):
    print(source, destination)
    if _ignore:
        if os.path.isfile(source):
            if not to_be_ignored(source):
                execute_bash("cp " + source + " " + destination + " -p")
        else:
            new_dir = destination + '/' + source.split('/')[0]
            execute_bash("mkdir " + new_dir)
            for element in os.listdir(source):
                copy(source + '/' + element, new_dir)
    else:
        execute_bash("cp " + source + " " + destination + " -p")


def back_up_dir(source_dict: dict, destination_dict: dict):
    # {'t': 'd', 's': size, 'p': base_path, 'time': get_time(stats),'dirs': info}
    # {'t': 'f', 's': stats.st_size, 'p': full_path + '/' + entity, 'time': get_time(stats)}
    for entity in source_dict:
        if entity in destination_dict:
            if source_dict[entity]['time'] > destination_dict[entity]['time']:
                copy(source_dict[entity]['p'], destination_dict['p'])
        else:
            copy(source_dict[entity]['p'], destination_dict['p'])


def pull(source_path: str, destination_path: str, track_first: bool = True, ignore: bool = False) -> None:
    # source_path is a file or directory
    # destination_path is a directory
    global _source_path, _destination_path, source_structure, destination_structure, _ignore
    print("Starting Backup! Please don't turn off your computer till the process finishes.")
    _source_path = source_path
    _destination_path = destination_path
    _ignore = ignore
    if _ignore:
        get_ignore_list()
    if track_first:
        track(source_path, output=False)
        print("Tracked source")
    track(destination_path)
    print("Tracked destination")
    source_json_name = source_path.strip().split('/')[-1] + '.json'
    destination_json_name = destination_path.strip().split('/')[-1] + '.json'
    if not os.path.lexists(source_path + '/' + constants.save_folder_name + '/' + source_json_name):
        track(source_path, output=False)
    source_structure = read_from_json_file(source_path + '/' + constants.save_folder_name + '/' + source_json_name)
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
        source_name = source_path.strip().split('/')[-1]
        if dest_name == source_name:
            back_up_dir(source_structure, destination_structure)
        elif source_name in destination_structure['dirs']:
            back_up_dir(source_structure, destination_structure['dirs'][source_name])
        else:
            copy(source_path, destination_path)
    track(destination_path)
    # track(source_path)
    print("All file(s) have been backed-up successfully")


if __name__ == '__main__':  # only for testing
    from pprint import pprint as pp

    file_name = os.getcwd().split('/')[-1] + '.json'
    _data = read_from_json_file(os.getcwd() + '/' + constants.save_folder_name + '/' + file_name)
    pp(_data)
