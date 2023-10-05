import sys
import os
import file_parcing
import datetime
import xlwt

TITLES = ['Название ТВ', 'Год', 'CEC', 'Тип', 'HDMI 2.0', 'HDMI 1.4', 'Max. mode', 'VSDB 1.4 4K', 'BT2020YCC',  'HDR (ST/HLG)',
           'HDR10+', 'DeepColor 4:4:4', 'DeepColor 4:2:0', 'Other', 'Проблемный ТВ']
edid_files_list = []


def edid_file_parsing(file_name):
    if os.stat(file_name).st_size < 200:
        return f'{file_name} have no EDID data!'
    return file_parcing.parsing(file_name)


def get_files_from_dir(file_path):
    for edid_file in os.listdir(file_path):
        if edid_file.endswith('.txt'):
            edid_files_list.append(os.path.join(file_path, edid_file))


def get_folder():
    if len(sys.argv) <= 1:
        print('Please set folder with EDID files')
    else:
        path_to_files = sys.argv[1]
        if os.path.isdir(path_to_files):
            get_files_from_dir(path_to_files)
            return path_to_files
        else:
            print('ERROR: it\'s not folder =(')
    return ''


def generate_xlsx_file_name(dir_path):
    dt = datetime.datetime.now()
    name = f'result_{dt.year}{dt.month}{dt.day}_{dt.hour}{dt.minute}{dt.second}.xls'
    return os.path.join(dir_path, name)


def write_to_ecxel(edid, row, sheet):
    col = 0
    for data in edid:
        sheet.write(row, col, data)
        col += 1


if __name__ == '__main__':
    path = get_folder()
    if path:
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("EDID")
        write_to_ecxel(TITLES, 0, sheet)
        row = 1
        for file in edid_files_list:

            edid_data = edid_file_parsing(file)
            if isinstance(edid_data, str):
                write_to_ecxel([os.path.split(file)[1], 'no edid'], row, sheet)
            else:
                write_to_ecxel(edid_data.get_result(), row, sheet)
            row += 1
        book.save(generate_xlsx_file_name(path))
