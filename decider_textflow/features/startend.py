# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Hurenkind: Single Line at Page Start
Schusterjunge: Single Line at Page End
"""

import statistics
import typing

import configo
import iamraw
import protocol
import utila

import decider_textflow.features
import decider_textflow.utils


def work(
    headlines: str,
    text: str,
    textpositions: str,
    sizeandborders: str,
    headerfooter: str,
    magiccontent: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    driver = decider_textflow.features.textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        magiccontent=magiccontent,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_7620 = """\
Hurenkind: Einsame Zeile am Seitenanfang

Seite beginnt mit einsamer Zeile: **{{rawline}}**.

{darstellung/schriftbild#hurenkind}
"""
HURENKIND_BEFORE = configo.HV_INT_PLUS(default=120)

HURENKIND_LINEWIDTH = configo.HV_PERCENT_PLUS(default=90)

SECOND_FULL_LINE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)


def check_7620_lonely_page_start(linter: callable, driver):  # pylint:disable=R1260
    linewidth = textwidth(driver.text_chunks)
    hurenkind_maxwidth = linewidth * HURENKIND_LINEWIDTH
    text = decider_textflow.utils.page_chunks(driver.nomagic_text_chunks)
    for page, content in text:
        if len(content) < 2:
            continue
        if content[0] is None or content[1] is None:
            continue
        first_headline = isinstance(content[0], iamraw.Headline)
        second_headline = isinstance(content[1], iamraw.Headline)
        if first_headline and second_headline:
            continue
        if not first_headline:
            if content[0].bounding.y0 > HURENKIND_BEFORE:
                # this page does not start with text line, there is may a
                # figure, table or something before.
                continue
        if second_headline and not first_headline:
            if content[1].decoration is not None:
                # CHAPTER-X-Pattern
                # Title
                continue
            # hurenkind
            # TEXT -> HEADLINE
            location = iamraw.RangedLocation(page=page, line=0)
            linter(
                location=location,
                rawline=content[0].text.strip(),
            )
            continue
        if not first_headline and not second_headline:
            # no headlines, text only
            first_width = width(content[0])
            second_width = width(content[1])
            second_full_line = utila.near(
                second_width,
                linewidth,
                diff=SECOND_FULL_LINE_DIFF_MAX,
            )
            if first_width <= hurenkind_maxwidth and second_full_line:
                # hurenkind
                # SHORT TEXT -> TEXT
                location = iamraw.RangedLocation(page=page, line=0)
                linter(
                    location=location,
                    rawline=content[0].text.strip(),
                )


SOLUTION_7621 = """\
Schusterjunge: Einsame Zeile am Seitenende

{darstellung/schriftbild#schusterjunge}
"""

SOLUTION_7625 = """\
Seitenanfang: Seite beginnt nicht mit Text

Die Grafik/Tabelle etc. sollte in den Text eingebunden werden und nicht \
direkt am Seitenanfang stehen.

{darstellung/schriftbild#seitenanfang}
"""

# TODO: ADD SUPPORT FOR TEXT ABOVE IMAGES/TABLE etc.

FAILSTART_MAX = configo.HV_INT_PLUS(default=100)


def check_7625_empty_start(linter: callable, driver):
    text = decider_textflow.utils.page_chunks(driver.nomagic_text_chunks)
    startend = page_startend(text)
    if startend is None:
        return
    start, _ = startend
    failstart = start + FAILSTART_MAX
    for page, content in text:
        if page_empty(content):
            continue
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
        linter(location=location)


def page_empty(content) -> bool:
    if all(item is None for item in content):
        # not all content is replaced with magic data, therefore None
        return True
    return False


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


STARTEND_PAGES_MIN = configo.HV_INT_PLUS(default=5)


def page_startend(items):  # pylint:disable=R1260
    if len(items) < STARTEND_PAGES_MIN:
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
    try:
        start = utila.mode(start)
        end = utila.mode(end)
    except statistics.StatisticsError:
        utila.error(f'disable `startend`: empty data {start} {end}')
        return None
    return start, end


def width(item):
    bounding = item.bounding
    return utila.roundme(bounding.x1 - bounding.x0)
