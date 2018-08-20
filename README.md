# fileTrackAndBackup
Track all the files and subdirectories of a folder. Also, quickly backup the whole folder.

### FEATURES:
* Track files and folders
* Simple command-line application
* See the whole folder structure, walking down the folder tree (detailed, visually simple, hierarchical format)
* Back-up whole folders in one go
* Back-up only selected folders/files (See [IGNORE](#ignore-filesfolders))

### SETUP:  
* Download this repo as a zip, or using `git pull`
* Unzip all the files in a folder
* Run `setup_ftb.py` (Note: you will have to run `setup_ftb.py` again, if you change the location of this project's folder)
* Optionally, add this project's folder location to the environment variable: PATH

### USAGE:
1. To track a file/folder (Also shows brief information about the file/folder):  
`file_tb.py track [FILE/FOLDER] [OPTIONS]`  
FILE/FOLDER: The relative or absolute path of a file/folder to be tracked (the current folder by default)  
Options:  
`--ignore`: Ignore some files/folders (See [IGNORE](#ignore-filesfolders))

2. To print the file data/folder structure:  
`file_tb.py print [FILE/FOLDER] [OPTIONS]`  
FILE/FOLDER: The relative or absolute path of a file/folder (the current folder by default)  
Options:  
`--ignore`: Ignore some files/folders, while tracking (See [IGNORE](#ignore-filesfolders)))  
`--raw`: Print out the raw data of the file/folder(Just like it has been saved internally while tracking)  
`--no_track`: Will not track before printing the file data/folder structure

3. To pull/back-up a folder:  
`file_tb.py pull SOURCE [DESTINATION FOLDER] [OPTIONS]`  
OR  
`file_tb.py back_up SOURCE [DESTINATION FOLDER] [OPTIONS]`  
SOURCE: The relative or absolute path of a file/folder to be copied/backed-up    
DESTINATION FOLDER: The relative or absolute path of a folder where the SOURCE is to be copied (the current folder by default)  
Options:  
`--ignore`: Ignore some files/folders (See [IGNORE](#ignore-filesfolders))  
`--no_track`: Will not track the SOURCE before backing-up
`--copy_all`: Will force check for the presence of all files. The edit-time of files are considered, and edit-time of folders are disregarded.
(Useful to restore files gone missing from the destination anytime after the source is edited) (Recommended)

4. To untrack a file/folder:  
`file_tb.py untrack [FILE/FOLDER]`  
FILE/FOLDER: The relative or absolute path of a file/folder (the current folder by default)

### IGNORE FILES/FOLDERS:
The `--ignore` option can be used with the `track`, `pull` (`back_up`) and `print` commands.  
This option helps ignore a few files/folders, while tracking/backing-up.  
Usage:  
* Add regex patterns to the file ignore_regex.txt in the project folder (each pattern on a new line)
* Use the `--ignore` option while using the `track`, `pull` (`back_up`) and `print` commands
* Files/Folders matching any of the regex patterns will be ignored
(The `--ignore` option, when used with the `print` command, is useful only when combined with the `--no_track` option)

### WORKING:
* The `track` command iterates over the files/folders and subdirectories, and tracks down all files and folders 
(except if the `--ignore` option is used), walking down the folder tree
* The name, size, location and edit-time of each file, folder and subdirectory is stored in a json file inside a folder named
'.file_tb'
---
* The `print` command tracks the FILE/FOLDER before printing out the details, except if the `--no_track` option is used
* If the `print` command is used with a folder, all the files and subdirectories are printed out in a hierarchical format,
along with their size and edit-time
* If used with a file, it prints the file's name, size, edit-time, path and track-time
* The `--raw` option simply pretty-prints the contents of the json file
---
* The `pull` or `back_up` command does the following:
    1. Track the SOURCE (except if the `--no_track` command is used)
    2. Track the DESTINATION
    3. Iterate over each file and folder in the SOURCE folder tree. If it is not present in the DESTINATION, it is copied.  
    If it is already present in the DESTINATION, the edit-time of both the files/folders are compared; the latest file/folder is kept in the DESTINATION.  
    If the option `--copy_all` is used, the edit-time of folders is disregarded, and the edit-times of each and every file is checked; the latest file is kept in the DESTINATION. 
    4. Track the DESTINATION
---
* The `untrack` command deletes the json file

### PLEASE NOTE:
* This program works only on Linux systems. (Tested on Ubuntu 18.04.1 LTS)
* This program requires Python 3. (Tested on Python 3.6)
* The program will possibly fail or malfunction if files/folders containing spaces in their names are tried to be backed-up.
* The operations may take quite some time, if there are lots of files/folders.
* The words 'folder' and 'directory' are used interchangeably.
* The reported statistics are only because of those files, which are not ignored. (You may see a difference in the size, because of this)
* There may be some differences in the size of files and folders, because of the internal workings of the Operating System.
* Size differences may be present due to the json file created.  
