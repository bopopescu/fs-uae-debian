import traceback
from fsbc.util import unused
from fsui.qt import Qt, QWidget, QPainter
from .Widget import Widget


class Panel(QWidget, Widget):

    def __init__(self, parent, paintable=False):
        unused(paintable)
        QWidget.__init__(self, parent.get_container() if parent else None)
        self.init_widget(parent)
        self.layout = None
        self._painter = None

        # QWidget.__init__(self)
        # self.setParent(parent.get_container())
        # super(Panel, self).__init__(parent.get_container())
        # super().__init__()
        self.move(0, 2000)
        self.setAutoFillBackground(True)

    @property
    def size(self):
        return self.get_size()

    def on_left_down(self):
        pass

    def on_left_up(self):
        pass

    def on_left_dclick(self):
        pass

    def on_paint(self):
        pass

    def create_dc(self):
        from .DrawingContext import DrawingContext
        return DrawingContext(self._painter)

    def paintEvent(self, event):
        # if not self._paintable:
        #     #dc = wx.PaintDC(self)
        #     return
        
        self._painter = QPainter(self)
        self._painter.setRenderHint(QPainter.Antialiasing)
        try:
            self.on_paint()
        except Exception:
            traceback.print_exc()
        finally:
            self._painter = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_left_down()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_left_up()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.on_left_dclick()

    def showEvent(self, event):
        self.on_resize()

    def resizeEvent(self, event):
        self.on_resize()

    def enterEvent(self, _):
        self.on_mouse_enter()

    def leaveEvent(self, _):
        self.on_mouse_leave()

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass
