from fsui.qt import QPushButton, QSignal
from .Widget import Widget


class Button(QPushButton, Widget):

    activated = QSignal()

    def __init__(self, parent, label):
        label = "  " + label + "  "
        # self._widget = QPushButton(label, parent.get_container())
        QPushButton.__init__(self, label, parent.get_container())
        # Widget.__init__(self, parent)
        self.init_widget(parent)
        # self._widget.clicked.connect(self.__clicked)
        # if not System.macosx:
        #     self.set_min_height(28)
        self.clicked.connect(self.__clicked)

    def __clicked(self):
        self.on_activate()
        self.activated.emit()

    def on_activate(self):
        pass
