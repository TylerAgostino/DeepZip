import os
import sys
import zipfile

source_path_string = 'C:\\Users\\Tyler\\PycharmProjects\\DeepZip\\TestInput\\'
output_path_string = 'C:\\Users\\Tyler\\PycharmProjects\\DeepZip\\TestOutput\\'

source_path_normalized = os.path.normpath(source_path_string)
terminal_directories = []

# TODO: optional copy entire structure to temporary folder so we can delete as we go

for root, dirs, files in os.walk(source_path_normalized, topdown=False, onerror=None, followlinks=False):
    if len(dirs) == 0:  # If the current directory has no subdirectories, it is a terminal directory
        terminal_directories.append(root)

print terminal_directories
