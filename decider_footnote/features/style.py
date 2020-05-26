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

import configo
import protocol
import utila

import decider_footnote.footnote

MAX_HIGHNOTE_RISE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value
MAX_HIGHNOTE_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value

MAX_CONTENT_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    headerfooters = decider_footnote.footnote.load(footerheader, pages)
    footnotes = utila.flatten([item.content for item in headerfooters if item])
    fontconfig = decider_footnote.footnote.most_common_font(footnotes)

    for footer in headerfooters:
        # run linter for every page
        linting(footer, fontconfig, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        footer,
        fontconfig: decider_footnote.footnote.FootNoteStyle,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(footer.page)

    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        for item in footer.content:
            datum = protocol.driver(
                item=item,
                fontconfig=fontconfig,
            )
            checker(call, datum)


SOLUTION_2003 = """\
Fußnote {%number%} invalid highnote rise

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2003_invalid_highnote_rise(linter, driver):
    """Ensure that footnote fits to `common` footnote highnote numer rise."""
    item = driver.item
    current = item.style[0].rise
    expected = driver.fontconfig.highnote_rise

    if utila.near(current, expected, MAX_HIGHNOTE_RISE_DIFF):
        return

    linter(
        number=item.number,
        current=current,
        expected=expected,
    )


SOLUTION_2004 = """\
Fußnote {%number%}: invalid highnote size

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2004_invalid_hignote_size(linter, driver):
    """Ensure correct font size of highnote."""
    item = driver.item
    current = item.style[0].size
    expected = driver.fontconfig.highnote_size

    if utila.near(current, expected, MAX_HIGHNOTE_SIZE_DIFF):
        return

    linter(
        number=item.number,
        current=current,
        expected=expected,
    )


SOLUTION_2005 = """\
Fußnote {%number%}: invalid font family

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2005_invalid_highnote_fontfamily(linter, driver):
    """Ensure correct font family of highnote."""
    item = driver.item
    current = item.style[0].font
    expected = driver.fontconfig.highnote_fontid

    if current == expected:
        return

    linter(
        number=item.number,
        current=current,
        expected=expected,
    )


SOLUTION_2010 = """\
Fußnote {%number%}: invalid content size

Expected: {%expected%} != Current: {%current%}

{text/fussnote#formatierung}
"""


def check_2010_invalid_content_fontsize(linter, driver):
    """Ensure correct font size of footnote content."""
    item = driver.item
    expected = driver.fontconfig.content_size
    sizes = [item.size for item in item.style[1].content]
    sizes_equal = [
        utila.near(item, expected, MAX_CONTENT_SIZE_DIFF) for item in sizes
    ]

    if all(sizes_equal):
        return

    linter(
        number=item.number,
        current=sizes,
        expected=expected,
    )
