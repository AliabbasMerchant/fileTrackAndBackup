#!/usr/bin/env python3
from track import track
from pull import pull
from print_structure import print_structure
import sys
from help import *

# dict[file_name] = (type, size, full_path, time, stat)
# dict[dir_name] = (type, size, full_path, time, stat, dict)

constants.current_wd = os.getcwd()

if len(sys.argv) <= 1:
    display_help()
    raise AttributeError('Please enter appropriate command-line arguments')
else:
    if sys.argv[1] == 'track':
        base_path = constants.current_wd
        params = {'ignore': False}  # 'output': True

        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = os.getcwd() + '/' + sys.argv[2]  # is absolute path
            else:
                if sys.argv[2] in ['--ignore']:
                    pass
                else:
                    raise FileNotFoundError()

        base_path = base_path.replace('////', '/')  # safe-side
        base_path = base_path.replace('///', '/')  # safe-side
        base_path = base_path.replace('//', '/')

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

        os.chdir(constants.current_wd)

    elif sys.argv[1] == 'back_up' or sys.argv[1] == 'pull':
        pull_path = ''
        destination_path = constants.current_wd
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    pull_path = sys.argv[2]
                else:  # is relative path
                    pull_path = constants.current_wd + '/' + sys.argv[2]  # is absolute path
            else:
                raise FileNotFoundError()
        else:
            display_help()
            raise AttributeError('Please enter appropriate command-line arguments')
        if len(sys.argv) > 3:
            if os.path.lexists(sys.argv[3]):
                if str(sys.argv[3]).startswith('/'):  # is absolute path
                    destination_path = sys.argv[3]
                else:  # is relative path
                    destination_path = constants.current_wd + '/' + sys.argv[3]  # is absolute path
            else:  # maybe its --no_track
                pass
        if os.path.isdir(destination_path):
            params = {'ignore': False, 'track_first': True}
            if '--ignore' in sys.argv:
                params['ignore'] = True
            if '--no_track' in sys.argv:  # useless, maybe # may cause errors: not tested
                params['track_first'] = False
            pull(pull_path, destination_path, **params)
        else:
            raise AttributeError('Can back-up to a directory only. Cannot back-up to a file.')

    elif sys.argv[1] == 'print':
        base_path = constants.current_wd
        params = {'all': False, 'track_first': True, 'raw': False}

        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = os.getcwd() + '/' + sys.argv[2]  # is absolute path
            else:
                if sys.argv[2] in ['--all', '--no_track', '--raw']:
                    pass
                else:
                    raise FileNotFoundError()

        base_path = base_path.replace('////', '/')  # safe-side
        base_path = base_path.replace('///', '/')  # safe-side
        base_path = base_path.replace('//', '/')

        dir_path = base_path
        if os.path.isfile(base_path):
            dir_path = base_path[0: base_path.rindex('/')]
        os.chdir(dir_path)

        if '--all' in sys.argv:
            params['all'] = True
        if '--no_track' in sys.argv:  # useless, maybe # may cause errors: not tested
            params['track_first'] = False
        if '--raw' in sys.argv:
            params['raw'] = True
        print_structure(base_path, dir_path, **params)
        os.chdir(constants.current_wd)

    elif sys.argv[1] == 'untrack':
        base_path = constants.current_wd
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = os.getcwd() + '/' + sys.argv[2]  # is absolute path
            else:
                raise FileNotFoundError()

        base_path = base_path.replace('////', '/')  # safe-side
        base_path = base_path.replace('///', '/')  # safe-side
        base_path = base_path.replace('//', '/')

        if os.path.isfile(base_path):
            base_path = base_path[0: base_path.rindex('/')]
        os.chdir(base_path)

        execute_bash("rm -rf " + base_path + '/' + constants.save_folder_name)
        print(base_path + " is no longer tracked")
        os.chdir(constants.current_wd)

    else:
        display_help()
        raise AttributeError('Please enter appropriate command-line arguments')

# Errors:
# print Test
# untrack Test not working
