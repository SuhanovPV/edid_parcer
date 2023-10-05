class EDID:
    def __init__(self):
        self.tv_name = ''
        self.year = ''
        self.CEC = ""
        self.type = ""
        self.hdmi_20 = []
        self.hdmi_14 = []
        self.max_mode = ''
        self.VSDB_14_4K = False
        self.bt2020ycc = ''
        self.bt2020rgb = ''
        self.bt2020cycc = ''
        self.xvycc = ''
        self.hdr10 = ''
        self.hlg = ''
        self.st = ''
        self.dc_444 = []
        self.dc_420 = []

        self.video_data_block = []
        self.YCbCr_420_Video_Data_Block = []
        self.YCbCr_420_Capability_Map_Data_Block = []
        self.VSDB_14 = []
        self.tv_problems = []

    def get_max_mode(self):
        all_block = self.video_data_block + self.YCbCr_420_Video_Data_Block + self.YCbCr_420_Capability_Map_Data_Block
        video_DB_3840_2160 = list(set(self.find_resolution('3840x2160', 'p', *self.video_data_block)))
        YCbCr_420_Video_DB_3840_2160 = list(
            set(self.find_resolution('3840x2160', 'p', *self.YCbCr_420_Video_Data_Block)))
        YCbCr_420_Capability_Map_DB_3840_2160 = list(set(self.find_resolution('3840x2160', 'p',
                                                                              *self.YCbCr_420_Capability_Map_Data_Block)))

        if not video_DB_3840_2160 and not YCbCr_420_Video_DB_3840_2160 and not \
                YCbCr_420_Capability_Map_DB_3840_2160 and self.find_resolution('4096x2160', 'p', *all_block):
            self.tv_problems.append('4096x')
            return '4096x'

        if max(video_DB_3840_2160, default=0) >= 50 and max(YCbCr_420_Video_DB_3840_2160, default=0) < 50 and max(
                YCbCr_420_Capability_Map_DB_3840_2160, default=0) < 50:
            return f'2160p{",".join([str(x) for x in video_DB_3840_2160 if x >= 50])}Hz444'

        if max(video_DB_3840_2160, default=0) < 50 and max(YCbCr_420_Video_DB_3840_2160, default=0) >= 50 and max(
                YCbCr_420_Capability_Map_DB_3840_2160, default=0) < 50:
            return f'2160p{",".join([str(x) for x in YCbCr_420_Video_DB_3840_2160 if x >= 50])}Hz420'

        if max(video_DB_3840_2160, default=0) >= 50 and max(YCbCr_420_Video_DB_3840_2160, default=0) >= 50 or \
                max(video_DB_3840_2160, default=0) >= 50 and max(YCbCr_420_Capability_Map_DB_3840_2160,
                                                                 default=0) >= 50:
            freq = list(set(video_DB_3840_2160 + YCbCr_420_Video_DB_3840_2160 + YCbCr_420_Capability_Map_DB_3840_2160))
            return f'2160p{",".join([str(x) for x in freq if x >= 50])}Hz444,420'

        if max(video_DB_3840_2160, default=0) != 0 and max(video_DB_3840_2160, default=0) < 50:
            return f'2160p{",".join(str(x) for x in video_DB_3840_2160)}Hz'

        vsdb_4K = self.find_resolution('3840x2160', 'p', *self.VSDB_14)
        if not vsdb_4K and self.find_resolution('4096x2160', 'p', *self.VSDB_14):
            self.VSDB_14_4K = True
            self.tv_problems.append('4096xVSDB')
            return '4096xVSDB'
        if vsdb_4K:
            self.VSDB_14_4K = True
            self.tv_problems.append('3840xVSDB')
            return f'2160p{",".join([str(x) for x in vsdb_4K])}HzVSDB'

        video_DB_1080p = self.find_resolution('1920x1080', 'p', *self.video_data_block)
        if max(video_DB_1080p, default=0) >= 50:
            return f'1080p{",".join([str(x) for x in video_DB_1080p if x >= 50])}Hz'
        if max(video_DB_1080p, default=0) > 0:
            return f'1080p{",".join([str(x) for x in video_DB_1080p])}Hz'

        video_DB_1080i = self.find_resolution('1920x1080', 'i', *self.video_data_block)
        return f'1080p{",".join([str(x) for x in video_DB_1080i])}Hz'

    def find_resolution(self, resolution, scan, *list_resolution):
        return sorted([x['frequency'] for x in list_resolution if x['full_res'] == resolution and x['scan'] == scan])

    def get_hdmi_20_value(self):
        if len(self.hdmi_20) == 2:
            return f'{self.hdmi_20[1]}MHz'
        if len(self.hdmi_20) == 1:
            return 'No TMDS'
        if len(self.hdmi_20) == 0 and self.max_mode.startswith('1080'):
            return '-'
        else:
            return 'default'

    def get_hdmi_14_value(self):
        if len(self.hdmi_14) == 2:
            return f'{self.hdmi_14[1]} MHz'
        if len(self.hdmi_14) == 1:
            return 'No TMDS',
        if len(self.hdmi_14) == 0:
            self.tv_problems.append('no Vendor-Specific Data Block "OUI 00-0C-03"')
            return '(*r)'

    def convwert_boolt_to_symbol(self, val):
        if val:
            return 'Y'
        else:
            return ''

    def get_result(self):
        self.max_mode = self.get_max_mode()
        result = [self.tv_name,
                  self.year,
                  self.CEC,
                  self.type,
                  self.get_hdmi_20_value(),
                  self.get_hdmi_14_value(),
                  self.max_mode,
                  self.convwert_boolt_to_symbol(self.VSDB_14_4K),
                  self.convwert_boolt_to_symbol(self.bt2020ycc),
                  ', '.join([a for a in [self.hlg, self.st] if a != '']),
                  self.hdr10,
                  ','.join(self.dc_444),
                  ','.join(self.dc_420),
                  ', '.join([x for x in [self.bt2020rgb, self.bt2020cycc, self.xvycc] if x != '']),
                  ', '.join(self.tv_problems)
                  ]
        return result

    def __str__(self):
        TITLES = ['Название ТВ', 'Год', 'CEC', 'Тип', 'HDMI 2.0', 'HDMI 1.4', 'Max. mode', 'VSDB 1.4 4K', 'BT2020YCC',
                  'HDR (ST/HLG)', 'HDR10+', 'DeepColor 4:4:4', 'DeepColor 4:2:0', 'Other', 'Проблемный ТВ']
        result = self.get_result()
        return '\n'.join([f'{tup[0]}: {tup[1]}' for tup in zip(TITLES, result)])
