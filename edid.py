class EDID:
    def __init__(self):
        self.tv_name = ''
        self.year = ''
        self.CEC = ""
        self.hdmi_20 = []
        self.hdmi_14 = []
        self.max_mode = ''
        self.VSDT_14_4K = False
        self.bt2020ycc = False
        self.bt2020rgb = False
        self.bt2020cycc = False
        self.xvycc = False
        self.hdr10 = False
        self.hlg = False
        self.dc_444 = []
        self.dc_420 = []

        self.video_data_block = []
        self.YCbCr_420_Video_Data_Block = []
        self.YCbCr_420_Capability_Map_Data_Block = []
        self.VSDT_14 = []
        self.tv_is_problems = []

    def get_max_mode(self):
        all_block = self.video_data_block + self.YCbCr_420_Video_Data_Block + self.YCbCr_420_Capability_Map_Data_Block
        video_DB_3840_2160 = list(set(self.find_resolution('3840x2160', 'p', *self.video_data_block)))
        YCbCr_420_Video_DB_3840_2160 = list(
            set(self.find_resolution('3840x2160', 'p', *self.YCbCr_420_Video_Data_Block)))
        YCbCr_420_Capability_Map_DB_3840_2160 = list(set(self.find_resolution('3840x2160', 'p',
                                                                              *self.YCbCr_420_Capability_Map_Data_Block)))

        if not video_DB_3840_2160 and not YCbCr_420_Video_DB_3840_2160 and not \
                YCbCr_420_Capability_Map_DB_3840_2160 and self.find_resolution('4096x2160', 'p', all_block):
            self.tv_is_problems.append('4096x')
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
            return f'2160p{",".join(video_DB_3840_2160)}Hz'

        vsdb_4K = self.find_resolution('3840x2160', *self.VSDT_14)
        if not vsdb_4K and self.find_resolution('4096x2160', 'p', *self.VSDT_14):
            self.VSDT_14_4K = True
            self.tv_is_problems.append('4096xVSDB')
            return '4096xVSDB'
        if vsdb_4K:
            self.VSDT_14_4K = True
            return f'2160p{",".join(vsdb_4K)}HzVSDB'

        video_DB_1080p = self.find_resolution('1920x1080', 'p', *self.video_data_block)
        if max(video_DB_1080p, default=0) >= 50:
            return f'1080p{",".join([str(x) for x in video_DB_1080p if x >= 50])}Hz'
        if max(video_DB_1080p, default=0) > 0:
            return f'1080p{",".join([str(x) for x in video_DB_1080p if x >= 50])}Hz'

        video_DB_1080i = self.find_resolution('1920x1080', 'i', *self.video_data_block)
        return f'1080p{",".join([str(x) for x in video_DB_1080i])}Hz'

    def find_resolution(self, resolution, scan, *list_resolution):
        return sorted([x['frequency'] for x in list_resolution if x['full_res'] == resolution and x['scan'] == scan])

    def get_calc_parameters(self):
        self.max_mode = self.get_max_mode()

    def __str__(self):
        self.get_calc_parameters()
        return ''
