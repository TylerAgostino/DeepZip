import shutil
import tempfile
import os
import zipfile
import glob

source_path_string = 'X:\\Google Drive\\Documents\\DeepZip Test\\'
output_path_string = 'C:\\Users\\Tyler\\PycharmProjects\\DeepZip\\TestOutput\\'

maximum_zip_file_size = 10000000

source_path_normalized = os.path.normpath(source_path_string)


def finish_zip(zip_to_finish, current_root):
    zip_path = zip_to_finish.filename
    zip_to_finish.close()
    input_relative_path = current_root.replace(source_path_normalized, "")
    output_file_name = ''.join(
        char for char in str(input_relative_path) if char in valid_filename_characters)
    if output_file_name == '':  # Zip file contains entire source directory, so we will name it after the source itself
        output_file_name = os.path.dirname(source_path_normalized)
        output_file_name = output_file_name.replace(os.path.dirname(output_file_name) + '\\', "")
    output_file_full_path = os.path.normpath(output_path_string + output_file_name)
    existing_zips_with_same_name = len(glob.glob(output_file_full_path + '*'))
    if existing_zips_with_same_name > 0:
        output_file_full_path = output_file_full_path + str(existing_zips_with_same_name)
    shutil.copy(zip_path, output_file_full_path + '.zip')
    os.remove(zip_path)


def start_new_zip():
    new_zip_object = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    new_zip_path = new_zip_object.name
    new_zip_object.close()
    new_zip = zipfile.ZipFile(new_zip_path, 'a', zipfile.ZIP_DEFLATED)
    return new_zip


zip_file_is_full = False
at_top_level = False
temporary_zip = start_new_zip()
zip_content_details = temporary_zip.infolist()
total_compressed_size = 0
total_uncompressed_size = 0

valid_filename_characters = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'

for root, dirs, files in os.walk(source_path_normalized, topdown=False, onerror=None, followlinks=False):
    for file_to_be_compressed in files:
        current_zip_path = temporary_zip.filename
        current_zip_size = os.path.getsize(current_zip_path)
        next_file_size = os.path.getsize(root + '\\' + file_to_be_compressed)
        if current_zip_size + next_file_size > maximum_zip_file_size and current_zip_size > 0:
            finish_zip(temporary_zip, root)
            temporary_zip = start_new_zip()
        relative_root = root.replace(os.path.dirname(source_path_normalized) + '\\', "")
        temporary_zip.write(root+'\\'+file_to_be_compressed, relative_root+'\\'+file_to_be_compressed)

finish_zip(temporary_zip, root)
