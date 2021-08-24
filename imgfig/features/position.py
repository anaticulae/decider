# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol
import serializeraw
import textflow.alignment.style
import utila

import imgfig.features.quality


def work(border: str, *images: str, pages: tuple = None) -> protocol.ResultType:
    contentborder = serializeraw.load_pageborders(border, pages=pages)
    driver = imgfig.features.quality.create_driver(
        *images,
        contentborder=contentborder,
        pages=pages,
    )
    if not driver.images:  # pylint:disable=E1101
        # document without images, nothing to lint, return empty result
        return protocol.RESULT_EMPTY
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_4030 = """\
Erwartete Ausrichtung der Abbildung nicht ermittelbar

Es wurden Abbildungen {{count}} gefunden. Diese scheinen willkürlich \
ausgerichtet. Sorgen Sie für eine einheitliche Ausrichtig(links, \
zentriert, rechts).
"""


def check_4030_image_alignment_selection(linter: callable, driver):
    expected = expected_alignment(
        driver.images,
        contentborder=driver.contentborder,
    )
    if expected is None:
        utila.debug(f'too few images: {len(driver.images)}, disable 4030')
        return
    if expected != textflow.alignment.style.TextAlignment.UNDEFINED:
        # everything is fine
        return
    linter(
        location=protocol.OVERVIEW,
        count=len(driver.images),
    )


SOLUTION_4031 = """\
Abbildungen nicht einheitlich ausgerichtet

Erwartete Ausrichtung: {{expected}}
Gefundene Ausrichtung: {{current}}
"""
SOLUTION_4041_PAGE_MIN = 5


def check_4031_image_alignment_per_image(linter: callable, driver):
    expected = expected_alignment(
        driver.images,
        contentborder=driver.contentborder,
    )
    if expected is None:
        utila.debug(f'too few images: {len(driver.images)}, disable 4030')
        return
    if expected == textflow.alignment.style.TextAlignment.UNDEFINED:
        utila.debug('undefined image alignment, disable 4030')
        return
    for imageinfo in driver.images:
        if imageinfo.page < SOLUTION_4041_PAGE_MIN:
            # exclude title page from image judgement
            continue
        location = iamraw.BoundingLocation.fromtuple(
            bounding=imageinfo.bounding,
            page=imageinfo.page,
        )
        border = utila.select_page(driver.contentborder, page=imageinfo.page)
        leftright = (border.border.left, border.border.right)
        current = alignment(imageinfo.bounding, leftright)
        if current == expected:
            continue
        linter(location=location, current=current, expected=expected)


ALIGNMENT_TRUST_MIN = 0.6


def expected_alignment(images, contentborder, mincount: int = 5):
    textstyle = textflow.alignment.style.TextAlignment
    alignments = []
    for item in images:
        border = utila.select_page(contentborder, page=item.page)
        leftright = (border.border.left, border.border.right)
        current = alignment(item.bounding, leftright)
        alignments.append(current.value)
    if len(alignments) < mincount:
        return None
    left, center, right = utila.roundme([
        len([item for item in alignments if item == current]) /
        len(alignments) for current in range(3)
    ])
    if left > ALIGNMENT_TRUST_MIN:
        return textstyle.LEFT
    if center > ALIGNMENT_TRUST_MIN:
        return textstyle.CENTER
    if right > ALIGNMENT_TRUST_MIN:
        return textstyle.RIGHT
    return textstyle.UNDEFINED


def alignment(bounding, leftright: tuple):
    """\
    >>> alignment((354.35, 84.28, 495.62, 268.78), (69.38, 527.85))
    <TextAlignment.RIGHT: ...>
    """
    left, right = leftright
    leftdist, rightdist = bounding[0] - left, right - bounding[2]
    if rightdist < 50.0 and leftdist > 150.0:
        return textflow.alignment.style.TextAlignment.RIGHT
    if rightdist:
        rate = leftdist / rightdist
    else:
        rate = 0.0
    leftdist, rightdist, rate = utila.roundme((leftdist, rightdist, rate))
    if max((leftdist, rightdist)) > 10.0:
        if rate > 0.9:
            return textflow.alignment.style.TextAlignment.CENTER
    if leftdist < 5.0:
        return textflow.alignment.style.TextAlignment.LEFT
    return textflow.alignment.style.TextAlignment.UNDEFINED
