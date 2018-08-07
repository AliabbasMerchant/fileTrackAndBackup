import subprocess
import os


def execute_bash(command: str) -> (str, str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output is not None:
        output = output.decode('ascii')
    if error is not None:
        error = error.decode('ascii')
    return output, error


setup_commands = ['mkdir Test'
                  'touch Test/a.txt']
test_commands = ['file_ftb.py track',
                 'file_ftb.py track',
                 'file_ftb.py track Test',
                 'file_ftb.py track Test',
                 'file_ftb.py track Test_A',
                 'file_ftb.py track Test_A',

                 'file_ftb.py track --ignore',
                 'file_ftb.py track Test --ignore',
                 'file_ftb.py track Test_A --ignore',
                 
                 'file_ftb.py untrack',
                 'file_ftb.py untrack Test',
                 'file_ftb.py untrack Test_A',
                 'file_ftb.py untrack',
                 'file_ftb.py untrack Test',
                 'file_ftb.py untrack Test_A',
                 
                 'file_ftb.py print',
                 'file_ftb.py print Test',
                 'file_ftb.py print Test_A',

                 'file_ftb.py print --all',
                 'file_ftb.py print Test --all',
                 'file_ftb.py print Test_A --all',

                 'file_ftb.py untrack',
                 'file_ftb.py untrack Test'

                 'file_ftb.py print --no_track',
                 'file_ftb.py print Test --no_track',
                 'file_ftb.py print Test_A --no_track',

                 'file_ftb.py print --raw',
                 'file_ftb.py print Test --raw',
                 'file_ftb.py print Test_A --raw',

                 'file_ftb.py print --raw --no_track',
                 'file_ftb.py print Test --raw --no_track',
                 'file_ftb.py print Test_A --raw --no_track',
                 ]

with open('errors.txt', 'w+') as f:
    for command in setup_commands:
        op, err = execute_bash(command)
        if err is not None:
            print(command + ":" + err)
            f.write(command + ":" + err)
            exit(1)

    for command in test_commands:
        op, err = execute_bash(command)
        if err is not None:
            print("ERROR:")
            f.write("ERROR:")
            f.write("\n")
            print(command + ":" + err)
            f.write(command + ":" + err)
            f.write("\n")
        else:
            print(command + ":" + op)
            f.write(command + ":" + op)
            f.write("\n")
