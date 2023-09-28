import os

from edid import EDID


def get_tv_name(name):
    tv_name = os.path.splitext(os.path.split(name)[1])[0].replace('_', ' ')
    return tv_name


def get_year(text):
    return text.rstrip()[-5:]


def get_resolution(text):
    res = text.split()
    resolution = dict()
    resolution['resolution'] = get_short_resolution(res[2])
    resolution['scan'] = get_scan(res[2])
    resolution['frequency'] = get_frequency(res[3])
    resolution['tmds'] = get_tmds(res[8])
    resolution['is_native'] = is_native(res[-1])
    return resolution


def get_short_resolution(res):
    short = res.split('x')[1]
    return int(short.replace('i', ''))


def get_scan(res):
    scan = 'p'
    if 'i' in res:
        scan = 'i'
    return scan


def get_frequency(res):
    return float(res).__round__()

def get_tmds(res):
    return float(res).__round__()

def is_native(res):
    return '(native)' == res

def parsing(edid_file):
    edid = EDID()
    edid.tv_name = get_tv_name(edid_file)
    with open(edid_file) as file:
        video_block = False
        for row in file:
            text = row.strip()
            if 'Made in' in text:
                edid.year = get_year(text)
            elif 'Video Data Block:' == text:
                video_block = True
            elif 'VIC' in text and video_block:
                edid.resolutions.append(get_resolution(text))
            elif 'Audio Data Block' in text:
                video_block = False
            elif 'BT2020YCC' in text:
                edid.bt2020ycc = True
            elif 'BT2020RGB' in text:
                edid.bt2020rgb = True
            elif 'BT2020cYCC' in text:
                edid.bt2020cycc = True
            elif 'xvYCC' in text:
                edid.xvycc = True
            elif 'HDR10' in text:
                edid.hdr10 = True
            elif 'HLG' in text:
                edid.hlg = True
            elif 'Supports YCbCr 4:4:4' in text:
                edid.ycbcr_444 = True
            elif 'Supports YCbCr 4:2:2' in text:
                edid.ycbcr_422 = True
            #TODO Add parcing for DeepColor
    return edid


if __name__ == '__main__':
    e_file = r'C:\Users\ssuxx\PycharmProjects\edid_parcer\tmp\HISENSE_50U7QF.txt'
    print(parsing(e_file))
