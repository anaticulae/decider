# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Hurenkind: Single Line at Page Start
Schusterjunge: Single Line at Page End
"""

import typing

import iamraw
import serializeraw
import utila

import decider_textflow.features
import decider_textstyle.utils


def work(
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        magiccontent: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    magiccontent = serializeraw.load_types(magiccontent, pages=pages)
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        pages=pages,
    )
    result = decider_textflow.features.linting(__name__, driver)
    return result


SOLUTION_7620 = """\
Hurenkind: Einsame Zeile am Seitenanfang

Seite beginnt mit einsamer Zeile.

{darstellung/schriftbild#hurenkind}
"""


def check_7620_lonely_page_start(linter: callable, driver):
    linewidth = textwidth(driver.text_chunks)
    hurenkind_maxwidth = linewidth * 0.9  # TODO: HOLY VALUE
    text = decider_textstyle.utils.page_chunks(driver.nomagic_text_chunks)
    for page, content in text:
        if len(content) < 2:
            continue
        if content[0] is None or content[1] is None:
            continue
        first_headline = isinstance(content[0], iamraw.Headline)
        second_headline = isinstance(content[1], iamraw.Headline)
        if first_headline and second_headline:
            continue
        if second_headline and not first_headline:
            # CHAPTER-X-Pattern
            # Title
            if content[1].decoration is not None:
                continue
        if second_headline and not first_headline:
            # hurenkind
            # TEXT -> HEADLINE
            location = iamraw.RangedLocation(page=page, line=0)
            linter(location)
            continue

        if not first_headline and not second_headline:
            first_width = width(content[0])
            second_width = width(content[1])
            # TODO: HOLY VALUE
            second_full_line = utila.near(second_width, linewidth, diff=5.0)
            if first_width <= hurenkind_maxwidth and second_full_line:
                # hurenkind
                # SHORT TEXT -> TEXT
                location = iamraw.RangedLocation(page=page, line=0)
                linter(location)
                continue


SOLUTION_7621 = """\
Schusterjunge: Einsame Zeile am Seitenende

{darstellung/schriftbild#schusterjunge}
"""

SOLUTION_7625 = """\
Seitenanfang: Seite beginnt nicht mit Text

Die Grafik/Tabelle etc. sollte in den Text eingebunden werden und nicht
direkt am Seitenanfang stehen.

{darstellung/schriftbild#seitenanfang}
"""

# TODO: ADD SUPPORT FOR TEXT ABOVE IMAGES/TABLE etc.


def check_7625_empty_start(linter: callable, driver):
    text = decider_textstyle.utils.page_chunks(driver.nomagic_text_chunks)
    startend = page_startend(text)
    if startend is None:
        return
    start, _ = startend
    failstart = start + 100  # TODO: HOLY VALUE
    for page, content in text:
        if isinstance(content[0], iamraw.Headline):
            # TODO: ADD CHECK TO CHECK HEADLINES
            continue
        # if not content[0]:
        #     # page starts with math content
        #     continue
        # TODO: HANDLE SINGLE ITEM ON PAGE
        if content[0]:
            # page starts with content, table, caption etc. will yield none
            first = content[0]
            if first.bounding.y0 <= failstart:
                continue
        location = iamraw.RangedLocation(page=page, line=0)
        linter(location)


SOLUTION_7626 = """\
Seitenende: Seite endet nicht mit Text

"""

# def check_7626_empty_end(linter: callable, driver):
#     # TODO: DO WE REQUIRE THIS TEST OR IS IT SOLVED VIA 7625?
#     pass


def textwidth(chunks) -> float:
    result = []
    for _, __, item in chunks:
        if item is None:
            continue
        if isinstance(item, iamraw.Headline):
            continue
        result.append(width(item))

    result = utila.mode(result)
    return result


STARTEND_MIN_PAGES = 5  # TODO: HOLY VALUE


def page_startend(items):
    if len(items) < STARTEND_MIN_PAGES:
        utila.error(f'disable `startend`: too few pages {len(items)}')
        return None
    start, end = [], []
    for _, content in items:
        if not content:
            continue
        first = content[0]
        if first is None:
            continue
        if not isinstance(first, iamraw.Headline):
            # TODO: ADD HEADLINE SUPPORT
            first = first.bounding.y0
            start.append(first)
        if len(content) == 1:
            continue
        last = content[-1]
        if last is None:
            continue
        if not isinstance(last, iamraw.Headline):
            # TODO: ADD HEADLINE SUPPORT
            last = last.bounding.y1
            end.append(last)
    start = utila.mode(start)
    end = utila.mode(end)
    return start, end


def width(item):
    bounding = item.bounding
    return utila.roundme(bounding.x1 - bounding.x0)
