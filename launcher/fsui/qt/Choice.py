from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from fsui.qt import QSize, QComboBox, QStandardItem, Signal
from .Widget import Widget


class Choice(QComboBox, Widget):

    item_selected = Signal(int)

    def __init__(self, parent, items=[]):
        QComboBox.__init__(self, parent.get_container())
        #Widget.__init__(self, parent)
        self.init_widget(parent)
        self.inhibit_change_event = False

        for i, item in enumerate(items):
            self.insertItem(i, item)

        if len(items) > 0:
            self.set_index(0)
        self.currentIndexChanged.connect(self.__current_index_changed)

    def add_item(self, label, icon=None):
        # item = QStandardItem(label)
        # if icon:
        #     item.setIcon(icon.qicon)
        # item.setSizeHint(QSize(-1, 24))
        if icon is not None:
            self.addItem(icon.qicon, label)
        else:
            self.addItem(label)

    def __current_index_changed(self):
        if not self.inhibit_change_event:
            # print("Choice.__current_index_changed")
            index = self.currentIndex()
            self.item_selected.emit(index)
            return self.on_change()

    def get_index(self):
        return self.currentIndex()

    def set_index(self, index, signal=False):
        try:
            if not signal:
                self.inhibit_change_event = True
            self.setCurrentIndex(-1 if index is None else index)
        finally:
            if not signal:
                self.inhibit_change_event = False

    def on_change(self):
        pass
