import fsui
from fsgs.context import fsgs
from ...Config import Config


class CustomOptionsPage(fsui.Panel):

    def __init__(self, parent):
        fsui.Panel.__init__(self, parent)
        self.layout = fsui.VerticalLayout()

        # self.layout.add_spacer(20)

        hor_layout = fsui.HorizontalLayout()
        self.layout.add(hor_layout, fill=True, expand=True)

        # hor_layout.add_spacer(20)
        self.text_area = fsui.TextArea(self, font_family="monospace")
        self.text_area.set_min_width(760)
        self.text_area.set_min_height(460)
        self.text_area.set_text(self.get_initial_text())
        hor_layout.add(self.text_area, fill=True, expand=True)
        # hor_layout.add_spacer(20)

        # self.layout.add_spacer(20)

        self.get_window().add_close_listener(self.on_close_window)

    def on_close_window(self):
        self.update_config()

    def on_close_button(self):
        self.end_modal(0)

    def update_config(self):
        text = self.text_area.get_text()
        for key in list(fsgs.config.values.keys()):
            if key not in Config.default_config:
                del fsgs.config.values[key]

        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("# You can write key = value pairs here"):
                continue
            parts = line.split("=", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                # if key in Config.no_custom_config:
                #     continue
                value = parts[1].strip()
                Config.set(key, value)

    def get_initial_text(self):
        text = DEFAULT_TEXT
        keys = fsgs.config.values.keys()
        for key in sorted(keys):
            if key in Config.no_custom_config:
                continue
            value = fsgs.config.values[key]
            if not value:
                continue
            text += "{0} = {1}\n".format(key, value)
        return text

DEFAULT_TEXT = """\
# You can write key = value pairs here to set FS-UAE options
# not currently supported by the user interface. This is only a
# temporary feature until the GUI supports all options directly.
#
# The options specified here will apply to this configuration only.

"""
