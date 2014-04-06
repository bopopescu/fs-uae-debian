from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import threading
from fsbc.signal import Signal as BaseSignal

main_thread_id = threading.current_thread().ident


class Signal(object):

    listeners = {}

    @classmethod
    def add_listener(cls, signal, listener):
        #cls.listeners.setdefault(signal, []).append(listener)
        BaseSignal(signal).connect(listener)

    @classmethod
    def remove_listener(cls, signal, listener):
        #cls.listeners[signal].remove(listener)
        BaseSignal(signal).disconnect(listener)

    @classmethod
    def broadcast(cls, signal, *args):
        if signal == "config":
            # temporary, while restructuring        
            from fsgs import fsgs
            key, value = args
            fsgs.signal.notify("fsgs:config:" + key, value)

        # if threading.current_thread().ident == main_thread_id:
        #     cls.do_broadcast(signal, *args)
        # else:
        #     def function():
        #         cls.do_broadcast(signal, *args)
        #     fsui.call_after(function)
        BaseSignal(signal).notify(*args)
