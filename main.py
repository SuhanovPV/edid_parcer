import sys
import os
import file_parcing

edid_files_list = []


def edid_file_parsing(file_name):
    if os.stat(file_name).st_size < 200:
        return f'{file_name} have no EDID data!'
    edid = file_parcing.parsing(file_name)
    return str(edid)


def get_files_from_dir(path):

    for file in os.listdir(path):
        if file.endswith('.txt'):
            edid_files_list.append(os.path.abspath(file))


def get_folder():
    if len(sys.argv) <= 1:
        print('Please set folder with EDID files')
        return
    else:
        path = sys.argv[1]
        if os.path.isdir(path):
            get_files_from_dir(path)
        else:
            print('ERROR: it\'s not folder =(')



if __name__ == '__main__':
    get_folder()
    print(edid_files_list)
