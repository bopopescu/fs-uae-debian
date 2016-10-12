import fsui


class Theme:

    __instance = None

    def __init__(self):
        self.title_font = fsui.Font("Noto Sans", 15)
        # self.title_color = fsui.Color(0x80, 0x80, 0x80)
        self.title_color = fsui.Color(0x44, 0x44, 0x44)
        self.title_background = fsui.Color(0xff, 0xff, 0xff)
        # self.title_separator_color = fsui.Color(0xe5, 0xe5, 0xe5)
        self.title_separator_color = fsui.Color(0xcc, 0xcc, 0xcc)
        self.window_background = fsui.Color(0xf2, 0xf2, 0xf2)
        # self.sidebar_background = fsui.Color(0xeb, 0xeb, 0xeb)
        self.sidebar_background = fsui.Color(0xe2, 0xe2, 0xe2)
        self.selection_background = fsui.Color(0x40, 0x80, 0xff)

        self.title_glow_color = None
        # self.title_glow_color = fsui.Color(0xff, 0xcc, 0xff, 0x80)

    @classmethod
    def instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance
