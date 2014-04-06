from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import six
import urllib
import xml.etree.ElementTree
from xml.etree.cElementTree import ElementTree, Element, SubElement, tostring

downloadable = {
    "bb433ea476dca6db52c1a9851c312307dda63010":
    "Cybernetix - The First Battle (1991)(Vision)(SW)[h BTTR].adf",
    "67334f9bf28b9e4ae4fb38d695689b3ff8414766":
    "Dogfight v1.1 (19xx)(R. Ling).adf",
    "ecd2f292d3f799cd67f6cf2632246836908da380":
    "Transplant.adf",
}

def find_downloadable_file(sha1):
    if sha1 in downloadable:
        return sha1_to_url(sha1)
    return None

def sha1_to_url(sha1):
    return "http://fs-uae.net/s/{0}/{1}/{2}".format(
            sha1[:2], sha1, urllib.quote(downloadable[sha1].encode("UTF-8")))

def builtin_configs():
    for config_dict in configurations:
        yield create_xml_from_config_dict(config_dict)

def create_xml_from_config_dict(config_dict):
    root = Element("config")
    root.set("uuid", config_dict["uuid"])

    name_node = SubElement(root, "name")
    name_node.text =config_dict["config_name"]

    game_node = SubElement(root, "game")
    game_node.set("uuid", config_dict["parent"])
    game_name_node = SubElement(game_node, "name")
    game_name_node.text = config_dict["game_name"]
    game_platform_node = SubElement(game_node, "platform")
    game_platform_node.text = config_dict["platform"]

    options_node = SubElement(root, "options")
    for key, value in six.iteritems(config_dict):
        if key in ["game_name", "platform", "config_name", "uuid", "parent"]:
            continue
        if key.startswith("file_"):
            continue
        option_node = SubElement(options_node, key)
        option_node.text = value

    for i in range(100):
        name = config_dict.get("file_{0}_name".format(i), "")
        if not name:
            break
        sha1 = config_dict.get("file_{0}_sha1".format(i), "")
        #url = config_dict.get("file_{0}_url".format(i), "")
        url = sha1_to_url(sha1)
        file_node = SubElement(root, "file")
        file_name_node = SubElement(file_node, "name")
        file_name_node.text = name
        file_sha1_node = SubElement(file_node, "sha1")
        file_sha1_node.text = sha1
        file_url_node = SubElement(file_node, "url")
        file_url_node.text = url

    name = "{0} ({1}, {2})".format(config_dict["game_name"],
            config_dict["platform"], config_dict["config_name"])
    print(tostring(root))
    return name, tostring(root)

configurations = [

# http://aminet.net/game/2play/BlitzBombers.readme
#
# Short:        It's BLITZBOMBERS. And it's FREE.
# Author:       redwhen@ldngedge.demon.co.uk (Red When Excited)
# Uploader:     Big Will Riker ldngedge demon co uk (Steve Matty)
# Type:         game/2play
# Architecture: m68k-amigaos
#
# It's FINALLY here. The game some, or even a LOT people have
# been craving for. It's FREE as well.
#
# It's a snapshot of the game, as it was, back in January 1996 -
# when it was 98% complete. There are some quirks, but hey.
#
# Download and enjoy. Major bugs will probably get fixed.
#
# It requires an AGA Amiga, needs at LEAST 1.5Mb ChipRAM to run.
# FastRAM and/or accelerator will help when using lots of CPU
# players, or the serial link.
#
# http://www.ldngedge.demon.co.uk   is the place for FAQ's,
# patches etc.
#
# Have fun.

{
"uuid":        "bf1b7659-bb30-44b0-83dd-bd2c428a4214",
"parent":      "c1bcb261-adad-5a51-8f25-c5575798e30b",
"game_name":   "Cybernetix: The First Battle",
"platform":    "Amiga",
"config_name": "Built-in, Shareware, Vision",
"kickstart":   "AROS",
"file_0_name": "Cybernetix - The First Battle (1991)(Vision)(SW)[h BTTR].adf",
"file_0_sha1": "bb433ea476dca6db52c1a9851c312307dda63010",
},

# Does not work with builtin AROS kickstart (WB problems)
#{
#"uuid":        "b52a2ddd-e314-4479-8019-575f7b7b0e7a",
#"parent":      "b11f7f00-1fd7-519a-a0b8-ae0309053d22",
#"game_name":   "Dogfight",
#"platform":    "Amiga",
#"config_name": "Built-in, Freeware, Richard Ling",
#"kickstart":   "AROS",
#"file_0_name": "Dogfight v1.1 (19xx)(R. Ling).adf",
#"file_0_sha1": "67334f9bf28b9e4ae4fb38d695689b3ff8414766",
#},

# Does not work with builtin AROS kickstart (freezes at title screen)
# "Downfall (Amiga, Freeware)":
# """<config uuid="2e1998fb-41e0-4f67-9f6a-e7cddfbadffb">
#   <name>Shareware</name>
#   <game uuid="1b6a5c73-eaad-5601-9875-0ad3498a220a">
#     <name>Downfall</name>
#     <platform>Amiga</platform>
#   </game>
#   <options>
#   <kickstart>AROS</kickstart>
#   </options>
#   <file>
#     <name>Downfall.adf</name>
#     <sha1>cc9ea0e8d1ae139ea5313d9b22eccc2e965744e2</sha1>
#     <url>http://fengestad.no/sha1/cc/cc9ea0e8d1ae139ea5313d9b22eccc2e965744e2</url>
#   </file>
# </config>
# """

{
"uuid":        "ecb3da72-86c4-4921-a2c4-34f2d9290380",
"parent":      "1adf9bd3-4113-520b-973e-3caaebae369e",
"game_name":   "Transplant",
"platform":    "Amiga",
"config_name": "Built-in, Freeware, Jumping Jack Flash",
"kickstart":   "AROS",
"file_0_name": "Transplant.adf",
"file_0_sha1": "ecd2f292d3f799cd67f6cf2632246836908da380",
},

]
