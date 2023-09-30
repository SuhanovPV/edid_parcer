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
    resolution['res_h'], resolution['res_v'] = resolution['full_res'].split('x')
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


#
def parsing(edid_file):
    edid = EDID()
    edid.tv_name = get_tv_name(edid_file)
    with open(edid_file) as file:
        block_1 = False
        video_block = False
        ycbcr420_video_data_block = False
        ycbcr_420_capability_map_data_block = False

        for row in file:
            text = row.strip()
            if 'Made in' in text:
                edid.year = get_year(text)
            elif 'Video Data Block:' == text:
                video_block = True
            elif 'VIC' in text and video_block:
                edid.video_data_block.append(get_resolution_param(text))
            elif 'YCbCr 4:2:0 Video Data Block' in text:
                ycbcr420_video_data_block = True
            elif 'VIC' in text and ycbcr420_video_data_block:
                edid.YCbCr_420_Video_Data_Block.append(get_resolution_param(text))
            elif 'YCbCr 4:2:0 Capability Map Data Block' in text:
                ycbcr_420_capability_map_data_block = True
            elif 'VIC' in text and ycbcr_420_capability_map_data_block:
                edid.YCbCr_420_Capability_Map_Data_Block.append(get_resolution_param(text))
            elif 'Block 1' in text:
                block_1 = True
            elif 'DTD' in text and block_1:
                edid.VSDT_14.append(get_resolution_param(text))
            elif 'Source physical address:' in text:
                edid.CEC = True
            elif 'OUI 00-0C-03' in text:
                edid.hdmi_14.append(True)
            elif 'OUI C4-5D-D8' in text:
                edid.hdmi_20.append(True)
            elif 'Maximum TMDS clock' in text:
                edid.hdmi_14.append(get_tmds(text))
            elif 'Maximum TMDS Character Rate' in text:
                edid.hdmi_20.append(get_tmds(text))

            else:
                video_block = False
                ycbcr420_video_data_block = False
                ycbcr_420_capability_map_data_block = False
        edid.get_calc_parameters()

#             elif 'BT2020YCC' in text:
#                 edid.bt2020ycc = True
#             elif 'BT2020RGB' in text:
#                 edid.bt2020rgb = True
#             elif 'BT2020cYCC' in text:
#                 edid.bt2020cycc = True
#             elif 'xvYCC' in text:
#                 edid.xvycc = True
#             elif 'HDR10' in text:
#                 edid.hdr10 = True
#             elif 'HLG' in text:
#                 edid.hlg = True

#             #TODO Add parcing for DeepColor
#     return edid


if __name__ == '__main__':
    e_file = r'D:\python\edid_parcer\tmp\HISENSE_50U7QF.txt'
    parsing(e_file)
    e_file = r'D:\python\edid_parcer\tmp\LG_43NANO766QA.txt'
    parsing(e_file)
