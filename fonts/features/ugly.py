# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This is the uGLy-font detector"""

from typing import Set

from serializeraw import load_font_content
from serializeraw import load_font_header
from utila import Flag
from utila import file_read
from yaml import dump


def work(uglypath: str, header: str, content: str) -> str:
    """Determine ugly fonts based on a conifguration file `uglypath` which
    contains the font types which are `known` as ugly"""
    uglyfonts = load_ugly(uglypath)
    header = load_font_header(header)
    content = load_font_content(content)

    result = ugly(header, uglyfonts)
    dumped = dump(result)
    return dumped


def ugly(header, ugly_fonts: Set[str]):
    result = []
    for item in header:
        fontname = item.name
        if fontname in ugly_fonts:
            result.append({
                'font': fontname,
                'scale': item.scale,
                'description': 'Do not use this peace of $h!t'
            })
    return result


def load_ugly(path: str):
    """Load ugly file

    Every line of the ugly file is interpreted as ugly font. Comments are
    marked with an #.
    """
    # TODO: Support description with internet-links for the uglyness of the
    # font

    content = file_read(path)
    ugly_fonts = [
        item for item in content.splitlines() if item and '#' not in item
    ]
    return set(ugly_fonts)


def name():
    return 'uglyfonts'


def commandline():
    return Flag(longcut=name(), message='Extract ugly fonts out of font header')
