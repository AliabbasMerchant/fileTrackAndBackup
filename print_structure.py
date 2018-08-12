from help import *
from track import track
from pprint import pprint as pp
import datetime


def print_dir(data: dict, level: int) -> None:
    for name in data.keys():
        if data[name]['t'] == 'f':
            if level > 0:
                for i in range(3 * (level - 1)):
                    print(' ', end='')
                print('|__', end='')
            print(name, "(Size: {}, Edit_Time: {})"
                  .format(get_size_format(data[name]['s']),
                          datetime.datetime.fromtimestamp(data[name]['time'])))
    for name in data.keys():
        if data[name]['t'] == 'd':
            if level > 0:
                for i in range(3 * (level - 1)):
                    print(' ', end='')
                print('|__', end='')
            print(name, "(Size: {}, Edit_Time: {})"
                  .format(get_size_format(data[name]['s']),
                          datetime.datetime.fromtimestamp(data[name]['time'])))
            print_dir(data[name]['dirs'], level + 1)


def print_structure(path: str, dir_path: str, track_first: bool = True, raw: bool = False, ignore: bool = False) -> None:
    if track_first:
        track(path, dir_path, output=False, ignore=ignore)
    if os.path.isfile(path):
        filename = path.split('/')[-1]
        print('Name: {}'.format(filename))
        print('Track Time: {}'.format(datetime.datetime.fromtimestamp(
            datetime.datetime.timestamp(datetime.datetime.now()))))
        print('Size: {}'.format(get_size_format(os.stat(filename).st_size)))
        print('Path: {}'.format(path))
        print('Edit Time: {}'.format(datetime.datetime.fromtimestamp(get_time(os.stat(path)))))
    elif os.path.isdir(path):
        filename = path.split('/')[-1] + '.json'
        try:
            data = read_from_json_file(dir_path + '/' + constants.save_folder_name + '/' + filename)
        except FileNotFoundError:
            raise FileNotFoundError("The folder is not tracked. Please track it first")
        if raw:
            pp(data)
        else:
            print('Name: {}'.format(data['n']))
            print('Track Time: {}'.format(datetime.datetime.fromtimestamp(data['ts'])))
            print('Size: {}'.format(get_size_format(data['i']['s'])))
            print('Path: {}'.format(data['i']['p']))
            print('Edit Time: {}'.format(datetime.datetime.fromtimestamp(data['i']['time'])))
            print()
            print('Directory Structure:')
            dir_info = data['i']['dirs']
            print_dir(dir_info, 0)


if __name__ == '__main__':  # only for testing
    print_structure(os.getcwd(), os.getcwd(), track_first=False)
