import os
import file_parcing

PATH = dir_path = os.path.dirname(os.path.realpath(__file__))
EDID_DIR = os.path.join(PATH, 'tmp')
edid_files_list = []
for file in os.listdir(EDID_DIR):
    if file.endswith('.txt'):
        edid_files_list.append(os.path.join(EDID_DIR, file))


def edid_file_parsing(file_name):
    edid = file_parcing.parsing(file_name)
    return str(edid)


if __name__ == '__main__':
    s = 'Название ТВ\t\tГод\tCEC\tТип\tHDMI 2.0\tHDMI 1.4\tVSDB 1.4\t4k\tBT2020YCC\tHDR10\tHLG\tDeepColor 4:4:4\t' +\
        'DeepColor 4:2:0\tOther'
    f = open('result.txt', 'w')
    f.write(s+'\n')
    for file in edid_files_list:
        f.write(edid_file_parsing(file)+'\n')
    f.close()


