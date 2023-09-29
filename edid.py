class EDID:
    def __init__(self):
        self.tv_name = ''
        self.year = ''
        self.video_data_block = []
        self.YCbCr_420_Video_Data_Block = []
        self.YCbCr_420_Capability_Map_Data_Block = []
        self.tv_is_problem = False
        self.type = ''
        self.CEC = False
        self.hdmi_20 = []
        self.hdmi_14 = []
        self.max_mode = ''
        # self.tmds = dict()
        # self.vsdb_14 = False
        # self.bt2020ycc = False
        # self.bt2020rgb = False
        # self.bt2020cycc = False
        # self.xvycc = False
        # self.hdr10 = False
        # self.hlg = False
        # self.dc_444 = False
        # self.dc_420 = False
        # self.resolutions = []
        # self.max_resolution = dict()
        #

    def get_max_resolution(self, resolution):
        max_resolution = resolution[0]
        for res in resolution[1:]:
            if res['resolution'] > max_resolution['resolution']:
                max_resolution = res
            elif res['resolution'] == max_resolution['resolution']:
                if res['frequency'] > max_resolution['frequency']:
                    max_resolution = res
        return max_resolution

    def get_max_mode(self):
        total = self.find_resolution('3840x2160', *self.video_data_block, *self.YCbCr_420_Video_Data_Block,
                                     *self.YCbCr_420_Video_Data_Block)
        return total

    def find_resolution(self, resolution, *list_resolution):
        return [x for x in list_resolution if x['full_res'] == resolution]

    # def get_hdmi_version(self):
    #     if self.max_resolution['resolution'] == 4320:
    #         self.hdmi_version = '2.1'
    #     elif self.max_resolution['resolution'] == 2160 and self.max_resolution['frequency'] > 30:
    #         self.hdmi_version = '2.0'
    #     else:
    #         self.hdmi_version = '1.4'
    #
    # def is_deep_color(self):
    #     return self.dc_420 or self.dc_444

    def get_calc_parameters(self):
        self.max_mode = self.get_max_mode()
        self.tv_is_problem = self.is_problem()

    def is_problem(self):
        return self.tv_is_problem or not self.CEC

    def __str__(self):
        self.get_calc_parameters()
        return
