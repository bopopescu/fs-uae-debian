from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

#import sys
#macosx = (sys.platform == "darwin")

def get_parent(self):
    return self.GetParent()

def enable(self, enable=True):
    self.Enable(enable)

def disable(self):
    self.Enable(False)

def show(self, show=True):
    self.Show(show)

def show_or_hide(self, show):
    self.Show(show)

def hide(self):
    self.Show(False)

def is_visible(self):
    return self.IsShown()

def is_enabled(self):
    return self.IsEnabled()

def set_position(self, position):
    self.SetPosition(position)


def set_position_and_size(self, position, size):
    self.SetDimensions(position[0], position[1], size[0], size[1])
    #self.SetPosition(position)
    #self.SetSize(size)
    #self.set_position(position)
    #self.set_size(size)
    if hasattr(self, "layout") and self.layout is not None:
        #self.layout.set_position_and_size((0, 0))
        #self.layout.set_position_and_size(size)
        self.layout.set_size(size)

def set_size(self, size):
    self.SetSize(size)

#def get_min_width(self):
#    return self.GetBestSize()[0]

#def get_min_height(self):
#    return self.GetBestSize()[1]

#def set_fixed_width(self, width):
#    self.min_width = width
#
#def set_fixed_height(self, height):
#    self.min_height = height

def set_min_width(self, width):
    self.min_width = width

def set_min_height(self, height):
    self.min_height = height

def get_min_width(self):
    width = 0
    if hasattr(self, "min_width"):
        if self.min_width:
            width = max(self.min_width, width)
    if hasattr(self, "layout") and self.layout is not None:
        #return self.layout.get_min_width()
        width = max(self.layout.get_min_width(), width)
        return width
    return max(width, self.GetBestSize()[0])
    #return self.GetBestSize()[0]

def get_min_height(self):
    height = 0
    if hasattr(self, "min_height"):
        if self.min_height:
            height = max(self.min_height, height)
    if hasattr(self, "layout") and self.layout is not None:
        height = max(self.layout.get_min_height(), height)
        return height
    return max(height, self.GetBestSize()[1])

def focus(self):
    self.SetFocus()


def get_window(self):
    parent = None
    while self.parent:
        parent = self.parent
    return parent

def refresh(self):
    self.Refresh()

def get_background_color(self):
    from .Color import Color
    c= self.GetBackgroundColour()
    return Color(c.Red(), c.Blue(), c.Green())

def set_background_color(self, color):
    from .wxpython import wx
    self.SetBackgroundColour(wx.Colour(*color))

def set_tooltip(self, text):
    from .wxpython import wx
    self.SetToolTip(wx.ToolTip(text))

def popup_menu(self, menu, pos=(0, 0)):
    self.PopupMenu(menu._menu, pos)

names = [
    "disable",
    "enable",
    "focus",
    "get_background_color",
    "get_min_height",
    "get_min_width",
    "get_parent",
    "get_window",
    "hide",
    "is_visible",
    "is_enabled",
    "refresh",
    "set_background_color",
    "set_min_height",
    "set_min_width",
    "set_position_and_size",
    "set_position",
    "set_size",
    "set_tooltip",
    "show",
    "show_or_hide",
    "popup_menu",
]

def update_class(klass):
    for name in names:
        if not hasattr(klass, name):
            setattr(klass, name, globals()[name])
