# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import utila

import decider_imgfig.driver

DPI_MIN = configo.HV_FLOAT_PLUS(default=96.0)

DPI_MAX = configo.HV_FLOAT_PLUS(default=192.0)

RESOLUTION_DIFF_MAX = configo.HV_PERCENT_PLUS(default=5)


def work(*images: str, pages: tuple = None) -> protocol.ResultType:
    driver = decider_imgfig.driver.create(images=images, pages=pages)
    if not driver.images:  # pylint:disable=E1101
        # document without images, nothing to lint, return empty result
        return protocol.RESULT_EMPTY
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_4000 = """\
Auflösung zu niedrig

Das Bild weist eine zu geringe Auflösung auf und wird im Druck \
ungenügend erscheinen.

Gefunden: {{dpi}}
Erwartet: {{expected}}
"""


def check_4000_min_printing_resolution(linter: callable, driver):
    for imageinfo in driver.images:
        dpi = determine_resolution(imageinfo)
        if dpi[0] >= DPI_MIN and dpi[1] >= DPI_MIN:
            continue
        expected = DPI_MIN, DPI_MIN
        location = iamraw.BoundingLocation.fromtuple(
            bounding=imageinfo.bounding,
            page=imageinfo.page,
        )
        linter(dpi=dpi, expected=expected, location=location)


def determine_resolution(imageinfo):
    pdfwidth = utila.inch(utila.rectangle_width(imageinfo.bounding))
    pdfheight = utila.inch(utila.rectangle_height(imageinfo.bounding))

    width_dpi = utila.roundme(imageinfo.width / pdfwidth)
    height_dpi = utila.roundme(imageinfo.height / pdfheight)

    dpi = (width_dpi, height_dpi)
    return dpi


SOLUTION_4001 = """\
Auflösung unnötig hoch

Die Auflösung der Grafik sollte reduziert werden um den benötigen \
Speicher zu reduzieren.

Gefunden: {{dpi}}
Erwartet: kleiner als {{expected}}
"""


def check_4001_max_printing_resolution(linter, driver):
    for imageinfo in driver.images:
        dpi = determine_resolution(imageinfo)
        if dpi[0] <= DPI_MAX or dpi[1] <= DPI_MAX:
            continue
        expected = DPI_MAX, DPI_MAX
        location = iamraw.BoundingLocation.fromtuple(
            bounding=imageinfo.bounding,
            page=imageinfo.page,
        )
        linter(dpi=dpi, expected=expected, location=location)


SOLUTION_4002 = """\
Pixelgrafik

TODO: Add message here
"""

SOLUTION_4005 = """\
Grafik verzerrt

Das Seitenverhältnis der Grafik im Dokument entspricht nicht dem \
Ausgangzverhältnis und wird daher verzerrt dargestellt.

Druck: {{pdf}}
Quelle: {{image}}
"""


def check_4005_check_relation(linter, driver):
    for imageinfo in driver.images:
        # inch
        pdfwidth = utila.inch(utila.rectangle_width(imageinfo.bounding))
        pdfheight = utila.inch(utila.rectangle_height(imageinfo.bounding))
        # pdf
        pdf = utila.roundme(pdfwidth / pdfheight)
        image = utila.roundme(imageinfo.width / imageinfo.height)
        if utila.pnear(pdf, image, rel_tol=RESOLUTION_DIFF_MAX):
            continue
        location = iamraw.BoundingLocation.fromtuple(
            bounding=imageinfo.bounding,
            page=imageinfo.page,
        )
        linter(pdf=pdf, image=image, location=location)
