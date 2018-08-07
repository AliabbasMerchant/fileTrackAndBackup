from help import *
import constants
from track import track
from pprint import pprint as pp
import datetime
import copy

def print_dir(data: dict, level: int) -> None:
    for name in data.keys():
        if data[name]['type'] == 'file':
            if level > 0:
                for i in range(3*(level-1)):
                    print(' ', end='')
                print('|__', end='')
            print(name, "(Size: {} kB, Edit_Time: {})"
                  .format(data[name]['size'] / 1000, datetime.datetime.fromtimestamp(data[name]['edit_time'])))
    for name in data.keys():
        if data[name]['type'] == 'dir':
            if level > 0:
                for i in range(3*(level-1)):
                    print(' ', end='')
                print('|__', end='')
            print(name, "(Size: {} kB, Edit_Time: {})"
                  .format(data[name]['size'] / 1000, datetime.datetime.fromtimestamp(data[name]['edit_time'])))
            print_dir(data[name]['dirs'], level + 1)


def print_structure(path: str, all:bool=False, track_first: bool=True, raw: bool=False) -> None:
    if track_first:
        track(path, output=False)
    if os.path.isfile(path):
        filename = path.split('/')[-1].split('.')[0]
        print(filename, " :", os.stat(filename).st_size, "bytes")
    elif os.path.isdir(path):
        filename = path.split('/')[-1] + '.json'
        stop = False
        try:
            data = read_from_json_file(path + '/' + constants.save_folder_name + '/' + filename)
        except FileNotFoundError:
            stop = True
            print("The folder is not tracked. Please track it first")
        if stop:
            raise Exception()
        # data = data[max([int(x) for x in data.keys()])]
        if raw:
            if all:
                pp(data)
            else:
                pp(data[str(max([int(x) for x in data.keys()]))])
        else:
            if all:
                old_data = copy.deepcopy(data)
                indices = sorted([int(x) for x in data.keys()])
                for i in indices:
                    data = old_data[str(i)]
                    print('Index: {}'.format(i))
                    print('Name: {}'.format(data['name']))
                    print('Track Time: {}'.format(data['timestamp']))
                    print('Size: {} kB'.format(data['info']['size'] / 1000))
                    print('Path: {}'.format(data['info']['path']))
                    print('Edit_Time: {}'.format(datetime.datetime.fromtimestamp(data['info']['edit_time'])))
                    print()
                    print('Directory Structure:')
                    # print('Stats: {}'.format(data['info']['stats']))
                    dir_info = data['info']['dirs']
                    print_dir(dir_info, 0)
            else:
                data = data[str(max([int(x) for x in data.keys()]))]
                print('Name: {}'.format(data['name']))
                print('Track Time: {}'.format(data['timestamp']))
                print('Size: {} kB'.format(data['info']['size']/1000))
                print('Path: {}'.format(data['info']['path']))
                print('Edit_Time: {}'.format(datetime.datetime.fromtimestamp(data['info']['edit_time'])))
                print()
                print('Directory Structure:')
                # print('Stats: {}'.format(data['info']['stats']))
                dir_info = data['info']['dirs']
                print_dir(dir_info, 0)


if __name__ == '__main__':  # only for testing
    print_structure(os.getcwd(), track_first=False)