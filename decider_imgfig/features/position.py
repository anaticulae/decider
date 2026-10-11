# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import configos
import iamraw
import protoerror
import texmex
import utilo

import decider_imgfig.driver


def work(
    border: str,
    xdocinfo: str,
    *images: str,
    pages: tuple = None,
) -> protoerror.ResultType:
    driver = decider_imgfig.driver.create(
        images=images,
        contentborder=border,
        docinfo=xdocinfo,
        pages=pages,
    )
    if not driver.images:  # pylint:disable=E1101
        # document without images, nothing to lint, return empty result
        return protoerror.RESULT_EMPTY
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
        document=driver.docinfo,  # pylint:disable=E1101
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
        utilo.debug(f'too few images: {len(driver.images)}, disable 4030')
        return
    if expected != texmex.TextAlignment.UNDEFINED:
        # everything is fine
        return
    linter(
        location=protoerror.OVERVIEW,
        count=len(driver.images),
    )


SOLUTION_4031 = """\
Abbildungen nicht einheitlich ausgerichtet

Erwartete Ausrichtung: {{expected}}
Gefundene Ausrichtung: {{current}}
"""


@protoerror.section_skip(iamraw.sections.Abstract)
@protoerror.section_skip(iamraw.sections.LegalInformation)
@protoerror.section_skip(iamraw.sections.TitlePage)
def check_4031_image_alignment_per_image(linter: callable, driver):
    """Do not judge image positon in abstract, legal etc. There are
    often signatures or logos."""
    expected = expected_alignment(
        driver.images,
        contentborder=driver.contentborder,
    )
    if expected is None:
        utilo.debug(f'too few images: {len(driver.images)}, disable 4030')
        return
    if expected == texmex.TextAlignment.UNDEFINED:
        utilo.debug('undefined image alignment, disable 4030')
        return
    for imageinfo in driver.images:
        location = iamraw.BoundingLocation.fromtuple(
            bounding=imageinfo.bounding,
            page=imageinfo.page,
        )
        border = utilo.select_page(driver.contentborder, page=imageinfo.page)
        leftright = (border.border.left, border.border.right)
        current = alignment(imageinfo.bounding, leftright)
        if current == texmex.TextAlignment.BLOCK:
            # block is always right
            continue
        if current == texmex.TextAlignment.UNDEFINED:
            utilo.log(f'undefined image alignment: {imageinfo}, skip 4031')
            continue
        if current == expected:
            continue
        linter(location=location, current=current, expected=expected)


ALIGNMENT_TRUST_MIN = configos.HV_FLOAT_PLUS(default=0.5)


def expected_alignment(images, contentborder, mincount: int = 5):
    textstyle = texmex.TextAlignment
    alignments = []
    for item in images:
        border = utilo.select_page(contentborder, page=item.page)
        leftright = (border.border.left, border.border.right)
        current = alignment(item.bounding, leftright)
        alignments.append(current.value)
    alignments = [item for item in alignments if item != textstyle.BLOCK.value]
    if len(alignments) < mincount:
        return None
    left, center, right = utilo.roundme([
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
    >>> alignment((119.41, 185.91, 474.91, 287.16), (102.88, 498.13))
    <TextAlignment.CENTER: ...>
    >>> alignment((102.88, 557.02, 498.13, 636.52), (102.88, 498.13))
    <TextAlignment.BLOCK: ...>
    """
    left, right = leftright
    leftdist, rightdist = bounding[0] - left, right - bounding[2]
    pagewidth = right - left
    imagewidth = utilo.rect_width(bounding)
    if imagewidth > (pagewidth - 25):
        # image covers complete page or more than complete page
        return texmex.TextAlignment.BLOCK
    if rightdist < 50.0 and leftdist > 150.0:
        return texmex.TextAlignment.RIGHT
    if rightdist:
        rate = leftdist / rightdist
    else:
        rate = 0.0
    leftdist, rightdist, rate = utilo.roundme((leftdist, rightdist, rate))
    maxed = max((leftdist, rightdist))
    if maxed > 10.0:
        dist = math.fabs(leftdist - rightdist)
        if rate > 0.9 or dist < 20:
            return texmex.TextAlignment.CENTER
    if leftdist < 5.0:
        return texmex.TextAlignment.LEFT
    return texmex.TextAlignment.UNDEFINED
