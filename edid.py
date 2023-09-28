class EDID:
    def __init__(self):
        self.tv_name = ''
        self.year = ''
        self.type = ''
        self.hdmi_14 = False
        self.hdmi_22 = False
        self.vsdb_14 = False
        self.tmds = 0
        self.bt2020ycc = False
        self.bt2020rgb = False
        self.bt2020cycc = False
        self.xvycc = False
        self.hdr10 = False
        self.hlg = False
        self.dc_444 = False
        self.dc_420 = False
        self.ycbcr_444 = False
        self.ycbcr_422 = False
        self.resolutions = []

    def __str__(self):
        # TODO realize method. Now just print ZALUPA
        return 'ZALUPA:\t' + self.tv_name + '\t ' + self.year + self.type + str(self.resolutions)
