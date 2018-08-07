#!/usr/bin/env python3
import constants
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
        base_path = os.getcwd()
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = os.getcwd() + '/' + sys.argv[2]  # is absolute path
            else:
                if sys.argv[2] in ['--ignore']:
                    base_path = os.getcwd()
                else:
                    raise FileNotFoundError()
        else:
            base_path = os.getcwd()  # is absolute path
        if '--ignore' in sys.argv:
            track(base_path, output=True, ignore=True)
        else:
            track(base_path, output=True)

    elif sys.argv[1] == 'back_up':
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
        base_path = os.getcwd()
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = os.getcwd() + '/' + sys.argv[2]  # is absolute path
            else:
                if sys.argv[2] in ['--all', '--no_track', '--raw']:
                    base_path = os.getcwd()
                else:
                    raise FileNotFoundError()
        else:
            base_path = os.getcwd()
        params = {'all': False, 'track_first': True, 'raw': False}
        if '--all' in sys.argv:
            params['all'] = True
        if '--no_track' in sys.argv:  # useless, maybe # may cause errors: not tested
            params['track_first'] = False
        if '--raw' in sys.argv:
            params['raw'] = True
        print_structure(base_path, **params)

    elif sys.argv[1] == 'untrack':
        base_path = os.getcwd()
        if len(sys.argv) > 2:
            if os.path.lexists(sys.argv[2]):
                if str(sys.argv[2]).startswith('/'):  # is absolute path
                    base_path = sys.argv[2]
                else:  # is relative path
                    base_path = os.getcwd() + '/' + sys.argv[2]  # is absolute path
            else:
                raise FileNotFoundError()
        else:
            base_path = os.getcwd()  # is absolute path
        execute_bash("rm -rf " + base_path + '/' + constants.save_folder_name)
        print(base_path + " is no longer tracked")


# Errors:
# print Test
# untrack Test not working