import os
from edid import EDID


def get_tv_name(name):
    tv_name = os.path.splitext(os.path.split(name)[1])[0].replace('_', ' ')
    return tv_name


def get_year(text):
    return text.rstrip()[-5:]


def get_resolution_param(text):
    res = text.split()
    resolution = dict()
    resolution['full_res'] = res[2].replace('i', '')
    resolution['scan'] = get_scan(res[2])
    resolution['frequency'] = get_frequency(res[3])
    return resolution


def get_scan(res):
    scan = 'p'
    if 'i' in res:
        scan = 'i'
    return scan


def get_frequency(res):
    return float(res).__round__()


def get_tmds(text):
    return text.split()[-2]


def get_port(text):
    phrases = text.split(': ')
    if len(phrases) > 1:
        return phrases[1]
    else:
        return '-'


def get_deep_color_bits(text, need_conversation=False):
    if text != 'Y444':
        bit = int(text[:2])
        if need_conversation:
            bit = int(bit / 3)
    else:
        bit = 'Y444'
    return str(bit)


#
def parsing(edid_file):
    with open(edid_file) as file:
        edid = EDID()
        edid.tv_name = get_tv_name(edid_file)

        block_1 = False
        video_block = False
        ycbcr420_video_data_block = False
        ycbcr_420_capability_map_data_block = False
        is_VSDB_BLOCK = False

        for row in file:
            text = row.strip()
            if 'Made in' in text or 'Model year' in text:
                edid.year = get_year(text)
            elif 'Video Data Block:' == text:
                video_block = True
            elif 'VIC' in text and video_block:
                edid.video_data_block.append(get_resolution_param(text))
            elif 'YCbCr 4:2:0 Video Data Block' in text:
                is_VSDB_BLOCK = False
                ycbcr420_video_data_block = True
            elif 'VIC' in text and ycbcr420_video_data_block:
                edid.YCbCr_420_Video_Data_Block.append(get_resolution_param(text))
            elif 'YCbCr 4:2:0 Capability Map Data Block' in text:
                is_VSDB_BLOCK = False
                ycbcr_420_capability_map_data_block = True
            elif 'VIC' in text and ycbcr_420_capability_map_data_block:
                edid.YCbCr_420_Capability_Map_Data_Block.append(get_resolution_param(text))
            elif 'HDMI VIC ' in text and is_VSDB_BLOCK:
                edid.VSDB_14.append(get_resolution_param(text.replace('HDMI ', '')))
            elif 'Source physical address:' in text:
                edid.CEC = get_port(text)
            elif 'OUI 00-0C-03' in text:
                is_VSDB_BLOCK = True
                edid.hdmi_14.append(True)
            elif 'OUI C4-5D-D8' in text:
                is_VSDB_BLOCK = False
                edid.hdmi_20.append(True)
            elif 'Maximum TMDS clock' in text:
                edid.hdmi_14.append(get_tmds(text))
            elif 'Maximum TMDS Character Rate' in text:
                edid.hdmi_20.append(get_tmds(text))
            elif 'BT2020YCC' in text:
                edid.bt2020ycc = True
            elif 'BT2020RGB' in text:
                edid.bt2020rgb = 'BT2020RGB'
            elif 'BT2020cYCC' in text:
                edid.bt2020cycc = 'BT2020cYCC'
            elif 'xvYCC' in text:
                edid.xvycc = 'xvYCC'
            elif 'HDR10' in text or "SMPTE ST2084" in text:
                edid.hdr10 = True
            elif 'HLG' in text:
                edid.hlg = True
            elif 'DC_' in text:
                edid.dc_444.append(get_deep_color_bits(text.replace('DC_', ''), True))
            elif 'Deep Color 4:2:0' in text:
                edid.dc_420.append(get_deep_color_bits(text.replace('Supports ', '')))
            else:
                video_block = False
                ycbcr420_video_data_block = False
                ycbcr_420_capability_map_data_block = False
    return edid


if __name__ == '__main__':
    e_file = r'D:\python\edid_parcer\tmp\JVC_LT32M580.txt'
    print(parsing(e_file))

