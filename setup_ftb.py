#!/usr/bin/env python3
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


print("Welcome!")
print("Setting Up File_Transfer_Backup (file_tb)...")

with open('constants.py', 'a') as f:
    f.write("\n")
    f.write("base_path = '" + os.getcwd() + "'")
    f.write("\n")

print("Making executable file...")
op, err = execute_bash("chmod +rwx file_tb.py")
if err is not None:
    print("Sorry! We have encountered some error in the setup of File_transfer_backup.")
    # print("Please setup File_transfer_backup manually")
    exit(1)

path = os.environ["PATH"]
path = path + os.pathsep + os.getcwd()

print("You may want to add the folder '{}' to the environment variables".format(os.getcwd()))
print("After setting up the environment variable, File_Transfer_Backup can be used by typing file_tb.py")
