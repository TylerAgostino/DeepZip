import shutil
import tempfile
import os
import zipfile
import glob


def _finish_zip(zip_to_finish, output_dir, content_map_file):
    valid_filename_characters = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890.'
    zip_path = zip_to_finish.filename
    zip_to_finish.close()
    contents_list = zip_to_finish.infolist()
    content_paths = []
    for contained_file in contents_list:
        content_paths.append(contained_file.filename)
    longest_common_path = _longest_common_path(content_paths)
    longest_path_slashes_replaced = longest_common_path.replace('/', '.')
    output_file_name = ''.join(
        char for char in str(longest_path_slashes_replaced) if char in valid_filename_characters)
    if output_file_name.endswith('.'):
        output_file_name = output_file_name[:-1]  # Get rid of trailing dot if ended on a directory
    output_file_full_path = os.path.normpath(output_dir + output_file_name)
    existing_zips_with_same_name = len(glob.glob(output_file_full_path + '_*' + '.zip'))
    if existing_zips_with_same_name > 0 or os.path.isfile(output_file_full_path + '.zip'):
        output_file_full_path = output_file_full_path + '_' + str(existing_zips_with_same_name)
    shutil.copy(zip_path, output_file_full_path + '.zip')
    os.remove(zip_path)
    content_map_file.write(output_file_name + '.zip' + '\n')
    content_map_file.write('-------------------------\n')
    for content_path in content_paths:
        content_map_file.write(content_path + '\n')
    content_map_file.write('\n\n')


def _start_new_zip():
    new_zip_object = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    new_zip_path = new_zip_object.name
    new_zip_object.close()
    new_zip = zipfile.ZipFile(new_zip_path, 'a', zipfile.ZIP_DEFLATED)
    return new_zip


def _longest_common_path(paths):
    longest_path = ''
    for i in range(len(paths[0])):
        for j in range(len(paths[0])-i+1):
            if j > len(longest_path) and all(paths[0][i:i+j] in x for x in paths):
                longest_path = paths[0][i:i+j]
    longest_path_directory = longest_path.rsplit('/', 1)[0]
    return longest_path_directory


def zipsplit(input_directory, output_directory, max_size):
    content_map = open(output_directory + 'index.txt', 'w')
    content_map.write('ZipSplit Archive Contents\n')
    content_map.write('-------------------------\n\n\n')
    temporary_zip = _start_new_zip()
    source_path_normalized = os.path.normpath(input_directory)
    for root, dirs, files in os.walk(source_path_normalized, topdown=False, onerror=None, followlinks=False):
        for file_to_be_compressed in files:
            current_zip_path = temporary_zip.filename
            current_zip_size = os.path.getsize(current_zip_path)
            next_file_size = os.path.getsize(root + '\\' + file_to_be_compressed)
            if current_zip_size + next_file_size > max_size and current_zip_size > 0:
                _finish_zip(temporary_zip, output_directory, content_map)
                temporary_zip = _start_new_zip()
            relative_root = root.replace(os.path.dirname(source_path_normalized) + '\\', "")
            temporary_zip.write(root+'\\'+file_to_be_compressed, relative_root+'\\'+file_to_be_compressed)

    _finish_zip(temporary_zip, output_directory,content_map)
    content_map.close()
