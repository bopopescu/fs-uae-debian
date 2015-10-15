from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

from fsgs.mednafen.mednafen import MednafenRunner


class SuperNintendoRunner(MednafenRunner):

    CONTROLLER = {
        "type": "gamepad",
        "description": "Gamepad",
        "mapping_name": "supernintendo",
    }

    PORTS = [
        {
            "description": "1st Controller",
            "types": [CONTROLLER]
        }, {
            "description": "2nd Controller",
            "types": [CONTROLLER]
        },
    ]

    def __init__(self, fsgs):
        super().__init__(fsgs)

    # def mednafen_aspect_ratio(self):
    #     return 4.0 / 3.0

    def mednafen_input_mapping(self, port):
        if port == 0:
            return {
                "A": "snes.input.port1.gamepad.a",
                "B": "snes.input.port1.gamepad.b",
                "X": "snes.input.port1.gamepad.x",
                "Y": "snes.input.port1.gamepad.y",
                "L": "snes.input.port1.gamepad.l",
                "R": "snes.input.port1.gamepad.r",
                "UP": "snes.input.port1.gamepad.up",
                "DOWN": "snes.input.port1.gamepad.down",
                "LEFT": "snes.input.port1.gamepad.left",
                "RIGHT": "snes.input.port1.gamepad.right",
                "SELECT": "snes.input.port1.gamepad.select",
                "START": "snes.input.port1.gamepad.start",
            }
        elif port == 1:
            return {
                "A": "snes.input.port2.gamepad.a",
                "B": "snes.input.port2.gamepad.b",
                "X": "snes.input.port2.gamepad.x",
                "Y": "snes.input.port2.gamepad.y",
                "L": "snes.input.port2.gamepad.l",
                "R": "snes.input.port2.gamepad.r",
                "UP": "snes.input.port2.gamepad.up",
                "DOWN": "snes.input.port2.gamepad.down",
                "LEFT": "snes.input.port2.gamepad.left",
                "RIGHT": "snes.input.port2.gamepad.right",
                "SELECT": "snes.input.port2.gamepad.select",
                "START": "snes.input.port2.gamepad.start",
            }

    def mednafen_system_prefix(self):
        return "snes"

    # def mednafen_video_size(self):
    #     if self.is_pal():
    #         size = (256, 239)
    #     else:
    #         size = (256, 224)
    #     return size
