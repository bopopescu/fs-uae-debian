from fs_uae_launcher.ui.behaviors.amigaenablebehavior import AmigaEnableBehavior
import fsui as fsui
from ..CDManager import CDManager
from ..FloppyManager import FloppyManager
from ..I18N import gettext
from .FloppySelector import FloppySelector


class FloppiesGroup(fsui.Group):

    def __init__(self, parent, drives=2, cd_mode=False):
        fsui.Group.__init__(self, parent)
        self.layout = fsui.VerticalLayout()

        self.cd_mode = cd_mode
        self.num_drives = drives

        hori_layout = fsui.HorizontalLayout()
        self.layout.add(hori_layout, fill=True)

        if cd_mode:
            self.label = fsui.HeadingLabel(self, gettext("CD-ROM Drive"))
        else:
            self.label = fsui.HeadingLabel(self, gettext("Floppy Drives"))
        hori_layout.add(self.label, margin=10)
        hori_layout.add_spacer(0, expand=True)

        self.multi_select_button = fsui.Button(
            self, gettext("Multi-Select..."))
        if self.cd_mode:
            self.multi_select_button.set_tooltip(
                gettext("Add Multiple CD-ROMs at Once"))
        else:
            self.multi_select_button.set_tooltip(
                gettext("Add Multiple Floppies at Once"))
        AmigaEnableBehavior(self.multi_select_button)
        self.multi_select_button.activated.connect(self.on_multi_select_button)

        hori_layout.add(self.multi_select_button, margin_right=10)

        self.layout.add_spacer(0)

        self.selectors = []
        for i in range(drives):
            selector = FloppySelector(parent, i)
            if cd_mode:
                selector.set_cd_mode(True)
            self.selectors.append(selector)
            self.layout.add(selector, fill=True, margin=10)

    def on_multi_select_button(self):
        if self.cd_mode:
            CDManager.multiselect(self.get_window())
        else:
            FloppyManager.multiselect(self.get_window())

    def update_heading_label(self):
        if self.cd_mode:
            if self.num_drives > 1:
                self.label.set_text(gettext("CD-ROM Drives"))
            else:
                self.label.set_text(gettext("CD-ROM Drive"))
        else:
            self.label.set_text(gettext("Floppy Drives"))
