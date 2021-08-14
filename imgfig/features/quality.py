# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import serializeraw
import utila

MIN_DPI = 96
MAX_DPI = MIN_DPI * 2

MAX_RESOLUTION_DIFF = configo.HV_PERCENT_PLUS(5).value


def work(*images: str, pages: tuple = None) -> protocol.ResultType:
    driver = create_driver(*images, pages=pages)
    if not driver.images:  # pylint:disable=E1101
        # document without images, nothing to lint, return empty result
        return protocol.RESULT_EMPTY
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


def create_driver(*images, contentborder=None, pages: tuple = None):
    loaded = load_image_info(*images, pages=pages)
    result = []
    for image in loaded:
        if not utila.rectangle_width(image.bounding):
            utila.error(f'skip zero-width image: {image.bounding}')
            continue
        if not utila.rectangle_height(image.bounding):
            utila.error(f'skip zero-height image: {image.bounding}')
            continue
        result.append(image)
    return protocol.driver(images=result, contentborder=contentborder)


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
        if dpi[0] >= MIN_DPI and dpi[1] >= MIN_DPI:
            continue
        expected = MIN_DPI, MIN_DPI
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
        if dpi[0] <= MAX_DPI or dpi[1] <= MAX_DPI:
            continue
        expected = MAX_DPI, MAX_DPI
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
        if utila.pnear(pdf, image, rel_tol=MAX_RESOLUTION_DIFF):
            continue
        location = iamraw.BoundingLocation.fromtuple(
            bounding=imageinfo.bounding,
            page=imageinfo.page,
        )
        linter(pdf=pdf, image=image, location=location)


def load_image_info(
    *images: str,
    pages: tuple = None,
) -> iamraw.ImageInformations:
    loaded = [serializeraw.load_image_info(item) for item in images]
    result = [
        item for item in loaded if not utila.should_skip(item.page, pages)
    ]
    return result
