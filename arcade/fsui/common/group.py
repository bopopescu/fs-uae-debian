from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import weakref


class Group(object):

    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        if hasattr(parent, "_window"):
            self._window = parent._window
        self.position = (0, 0)
        # FIXME: should instead be closest "real" parent (panel, whatever)
        # self.get_window().add_destroy_listener(self.__on_destroy)

    # def __on_destroy(self):
    #     self.on_destroy()

    @property
    def parent(self):
        return self._parent()

    def is_visible(self):
        return True

    # def on_destroy(self):
    #     pass

    def get_window(self):
        return self.parent.get_window()

    def get_container(self):
        return self.parent.get_container()

    def get_min_width(self):
        return self.layout.get_min_width()

    def get_min_height(self):
        return self.layout.get_min_height()

    def set_position(self, position):
        self.position = position
        if self.layout:
            self.layout.set_position(position)

    def set_size(self, size):
        if self.layout:
            self.layout.set_size(size)

    def set_position_and_size(self, position, size):
        self.position = position
        if self.layout:
            self.layout.set_position_and_size(position, size)
