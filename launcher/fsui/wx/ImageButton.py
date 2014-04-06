from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from .wxpython import wx
from .common import update_class
from .System import System
from .Widget import Widget


class ImageButton(wx.BitmapButton, Widget):
    def __init__(self, parent, image):
        wx.BitmapButton.__init__(
            self, parent.get_container(), -1, image.bitmap)
        Widget.__init__(self)
        self.Bind(wx.EVT_BUTTON, self.__button_event)
        if not System.macosx:
            self.min_height = 26

    def set_image(self, image):
        self.SetBitmapLabel(image.bitmap)

    def on_activate(self):
        pass

    def __button_event(self, event):
        self.on_activate()

update_class(ImageButton)
