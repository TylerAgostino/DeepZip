import shutil
import tempfile
import os
import zipfile

source_path_string = 'X:\\Google Drive\\Documents\\DeepZip Test\\'
output_path_string = 'C:\\Users\\Tyler\\PycharmProjects\\DeepZip\\TestOutput\\'

maximum_zip_file_size = 1000

source_path_normalized = os.path.normpath(source_path_string)
terminal_directories = []

# TODO: optional copy entire structure to temporary folder so we can delete as we go

for root, dirs, files in os.walk(source_path_normalized, topdown=False, onerror=None, followlinks=False):
    if len(dirs) == 0:  # If the current directory has no subdirectories, it is a terminal directory
        terminal_directories.append(root + '\\')

# Add directories to a temporary zip file until completed, then copy to output path
temporary_directory = tempfile.gettempdir()

for zip_start in terminal_directories:
    temporary_zip_object = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    temporary_zip_path = temporary_zip_object.name
    temporary_zip_object.close()
    temporary_zip = zipfile.ZipFile(temporary_zip_path, 'a', zipfile.ZIP_DEFLATED)

    zip_file_is_full = False
    at_top_level = False
    zip_compression_ratio = 0
    next_dir_to_add = zip_start
    while not zip_file_is_full and not at_top_level:
        for root, dirs, files in os.walk(next_dir_to_add):
            relative_root = root.replace(os.path.dirname(source_path_normalized) + '\\', "")
            for file in files:
                current_zip_contents = temporary_zip.namelist()
                if relative_root.replace('\\', '/')+'/'+file not in current_zip_contents:
                    temporary_zip.write(root+'\\'+file, relative_root+'\\'+file)
        last_directory_added = next_dir_to_add
        if next_dir_to_add == source_path_normalized:
            at_top_level = True
        else:
            next_dir_to_add = os.path.dirname(next_dir_to_add)
            zip_content_details = temporary_zip.infolist()
            total_compressed_size = 0
            total_uncompressed_size = 0
            for zipinfo_obj in zip_content_details:
                total_compressed_size += zipinfo_obj.compress_size
                total_uncompressed_size += zipinfo_obj.file_size
            try:
                zip_compression_ratio = total_compressed_size/total_uncompressed_size
            except ZeroDivisionError:
                pass  # Will throw an error when all files are empty, which isn't an issue here

            next_level_estimated_size = os.path.getsize(next_dir_to_add) * zip_compression_ratio
            if next_level_estimated_size >= maximum_zip_file_size:
                zip_file_is_full = True

    for unfinished_directory in terminal_directories:
        if str(unfinished_directory).startswith(last_directory_added):
            terminal_directories.remove(unfinished_directory)

    temporary_zip.close()
    valid_filename_characters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    input_relative_path = last_directory_added.replace(source_path_normalized, "")
    output_file_name = ''.join(char for char in str(input_relative_path) if char in valid_filename_characters)
    if output_file_name == '':  # Zip file contains entire source directory, so we will name it after the source itself
        output_file_name = os.path.dirname(source_path_normalized)
        output_file_name = output_file_name.replace(os.path.dirname(output_file_name) + '\\', "") + '.zip'
    output_file_full_path = os.path.normpath(output_path_string + output_file_name)
    shutil.copy(temporary_zip_path, output_file_full_path)
    os.remove(temporary_zip_path)