import os
import file_parcing

PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
EDID_DIR = os.path.join(PATH, 'tmp')
edid_files_list = []
for file in os.listdir(EDID_DIR):
    if file.endswith('.txt'):
        edid_files_list.append(os.path.join(EDID_DIR, file))


def edid_file_parsing(file_name):
    # TODO realize parcing and output results
    print(file)


if __name__ == '__main__':
    for file in edid_files_list:
        edid_file_parsing(file)
