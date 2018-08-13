#!/usr/bin/env python3
from track import track
from pull import pull
from print_structure import print_structure
import sys
from help import *

# dict[file_name] = (type, size, full_path, time, stat)
# dict[dir_name] = (type, size, full_path, time, stat, dict)

current_wd = os.getcwd()

if len(sys.argv) <= 1:
    display_help()
    raise AttributeError('Please enter appropriate command-line arguments')
else:
    if sys.argv[1] == 'track':
        base_path = current_wd
        params = {'ignore': False}  # 'output': True

        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if os.path.isabs(str(sys.argv[2])):
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = current_wd + '/' + sys.argv[2]  # is absolute path
                    base_path = base_path.replace('//', '/')
            else:
                if sys.argv[2] in ['--ignore']:
                    pass
                else:
                    raise FileNotFoundError("Could not find the file/folder: {}".format(sys.argv[2]))

        dir_path = base_path
        if os.path.isfile(base_path):
            dir_path = base_path[0: base_path.rindex('/')]
        os.chdir(dir_path)

        if '--ignore' in sys.argv:
            params['ignore'] = True

        errors = track(base_path, dir_path, output=True, **params)
        if len(errors) > 0:
            print()
            print("The following files/folders do not exist:")
            for error in errors:
                print(error)
        os.chdir(current_wd)

    elif sys.argv[1] == 'back_up' or sys.argv[1] == 'pull':
        pull_path = ''
        destination_path = current_wd
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if os.path.isabs(str(sys.argv[2])):
                    pull_path = sys.argv[2]
                else:  # is relative path
                    pull_path = current_wd + '/' + sys.argv[2]  # is absolute path
                    pull_path = pull_path.replace('//', '/')
            else:
                raise FileNotFoundError("Could not find the file/folder: {}".format(sys.argv[2]))
        else:
            display_help()
            raise AttributeError('Please enter appropriate command-line arguments')
        if len(sys.argv) > 3:
            if os.path.lexists(sys.argv[3]):
                if os.path.isabs(str(sys.argv[3])):
                    destination_path = sys.argv[3]
                else:  # is relative path
                    destination_path = current_wd + '/' + sys.argv[3]  # is absolute path
                    destination_path = destination_path.replace('//', '/')
        if os.path.isdir(destination_path):
            params = {'ignore': False, 'track_first': True}
            if '--ignore' in sys.argv:
                params['ignore'] = True
            if '--no_track' in sys.argv:  # may cause errors
                params['track_first'] = False
            os.chdir(destination_path)
            errors = pull(pull_path, destination_path, **params)
            if len(errors) > 0:
                print()
                print("There was an error in copying the following files/folders:")
                for error in errors:
                    print(error)
            os.chdir(current_wd)
        else:
            raise AttributeError("Can back-up to a directory only. Cannot back-up to a file.")

    elif sys.argv[1] == 'print':
        base_path = current_wd
        params = {'track_first': True, 'raw': False, 'ignore': False}

        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = current_wd + '/' + sys.argv[2]  # is absolute path
                    base_path = base_path.replace('//', '/')
            else:
                if sys.argv[2] in ['--no_track', '--raw', '--ignore']:
                    pass
                else:
                    raise FileNotFoundError("Could not find the file/folder: {}".format(sys.argv[2]))

        dir_path = base_path
        if os.path.isfile(base_path):
            dir_path = base_path[0: base_path.rindex('/')]
        os.chdir(dir_path)

        if '--no_track' in sys.argv:  # may give wrong file list
            params['track_first'] = False
        if '--raw' in sys.argv:
            params['raw'] = True
        if '--ignore' in sys.argv:
            params['ignore'] = True
        print_structure(base_path, dir_path, **params)
        os.chdir(current_wd)

    elif sys.argv[1] == 'untrack':
        base_path = current_wd
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = current_wd + '/' + sys.argv[2]  # is absolute path
                    base_path = base_path.replace('//', '/')
            else:
                raise FileNotFoundError("Could not find the file/folder: {}".format(sys.argv[2]))

        if os.path.isfile(base_path):
            base_path = base_path[0: base_path.rindex('/')]
        os.chdir(base_path)

        execute_bash("rm -rf '" + base_path + "/" + constants.save_folder_name + "'")
        print(base_path + " is no longer tracked")
        os.chdir(current_wd)

    else:
        display_help()
        raise AttributeError('Please enter appropriate command-line arguments')

# Errors:
# print Test
# untrack Test not working
