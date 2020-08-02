# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw
import protocol
import serializeraw
import utila

MIN_DPI = 96
MAX_DPI = MIN_DPI * 2


def work(*images: str, pages: tuple = None) -> typing.Tuple[str, str]:
    loaded = load_image_info(*images, pages=pages)
    if not loaded:
        # document with imnages, nothing to lint, return empty result
        return '[]', '[]'

    linter = protocol.from_module(__name__)

    linting(loaded, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(imageinfos: iamraw.ImageInformations, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)

    for checker in checkers:
        for imageinfo in imageinfos:
            location = protocol.BoundingLocation.fromtuple(
                bounding=imageinfo.bounding,
                page=imageinfo.page,
            )
            call = functools.partial(
                linter.add_finding,
                msgid=checker.msgid,
                location=location,
            )
            checker(call, imageinfo)


SOLUTION_4000 = """\
Auflösung zu niedrig

Das Bild weist eine zu geringe Auflösung auf und wird im Druck
ungenügend erscheinen.

Gefunden: {%dpi%}
Erwartet: {%expected%}
"""


def check_4000_min_printing_resolution(linter, imageinfo):
    pdfwidth = point_toinch(imageinfo.bounding[2] - imageinfo.bounding[0])
    pdfheight = point_toinch(imageinfo.bounding[3] - imageinfo.bounding[1])

    width_dpi = utila.roundme(imageinfo.width / pdfwidth)
    height_dpi = utila.roundme(imageinfo.height / pdfheight)

    dpi = (width_dpi, height_dpi)

    if dpi[0] >= MIN_DPI and dpi[1] >= MIN_DPI:
        return

    expected = MIN_DPI, MIN_DPI
    linter(dpi=dpi, expected=expected)


SOLUTION_4001 = """\
Auflösung unnötig hoch

Die Auflösung der Grafik sollte reduziert werden um den benötigen
Speicher zu reduzieren.

Gefunden: {%dpi%}
Erwartet: kleiner als {%expected%}
"""


def check_4001_max_printing_resolution(linter, imageinfo):
    pdfwidth = point_toinch(imageinfo.bounding[2] - imageinfo.bounding[0])
    pdfheight = point_toinch(imageinfo.bounding[3] - imageinfo.bounding[1])

    width_dpi = utila.roundme(imageinfo.width / pdfwidth)
    height_dpi = utila.roundme(imageinfo.height / pdfheight)

    dpi = (width_dpi, height_dpi)

    if dpi[0] <= MAX_DPI or dpi[1] <= MAX_DPI:
        return

    expected = MAX_DPI, MAX_DPI
    linter(dpi=dpi, expected=expected)


SOLUTION_4002 = """\
Pixelgrafik

TODO: Add message here
"""

SOLUTION_4005 = """\
Grafik verzerrt

Das Seitenverhältnis der Grafik im Dokument entspricht nicht dem
Ausgangzverhältnis und wird daher verzerrt dargestellt.
"""


def load_image_info(
        *images: str,
        pages: tuple = None,
) -> iamraw.ImageInformations:
    loaded = [serializeraw.load_image_info(item) for item in images]
    result = [
        item for item in loaded if not utila.should_skip(item.page, pages)
    ]
    return result


# TODO: MOVE TO UTILA
def point_toinch(point: float, userspace: float = 1.0) -> float:
    """\
    >>> point_toinch(72)
    1.0
    """
    # TODO: CHECK USER SPACE
    scale = 72.0 / userspace
    result = point / scale
    return result
