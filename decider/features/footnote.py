# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import math
import typing

import configo
import protocol
import utila

import decider.footnote
import decider.utils

MAX_HIGHNOTE_RISE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value
MAX_HIGHNOTE_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value

MAX_CONTENT_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = decider.utils.from_module(__name__)

    headerfooters = decider.footnote.load(footerheader, pages)
    footnotes = utila.flatten([item.content for item in headerfooters if item])
    fontconfig = decider.footnote.most_common_font(footnotes)
    for footer in headerfooters:
        footnotes = [decider.footnote.validate(item) for item in footer.content]
        # run linter
        linting(footnotes, fontconfig, footer.page, linter)

    # TODO: FIX RETURN TYPE AFTER UPGRADING UTILA
    # TODO: FIX AFTER UPGRADING PROTOCOL
    dumped = protocol.dump_result(linter.result, unique=True)
    # TODO: FIX AFTER UPGRADING PROTOCOL
    return dumped[0], dumped[1]


# TODO: ADD GENERAL PACKAGE TO DEFINE UNIQUE IDS
FOOTER_CHECKER_ID = 20

NO_UPPERCASE_AT_START = 2001
NO_DOT_AT_END = 2002
INVALID_HIGHNOTE_RISE = 2003
INVALID_HIGHNOTE_SIZE = 2004
INVALID_HIGHNOTE_FONT_FAMILY = 2005

INVALID_CONTENT_SIZE = 2010


def linting(
        validated,
        fontconfig: decider.footnote.FootNoteStyle,
        page: int,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(page)

    def check_2001_no_uppercase_at_start():
        # item : decider.footnote.Validated
        for item in validated:
            if item.uppercase:
                continue
            linter.add_finding(
                location=location,
                msgid=NO_UPPERCASE_AT_START,
                number=item.content.number,
            )

    def check_2002_no_dot_at_end():
        # item : decider.footnote.Validated
        for item in validated:
            if item.ends:
                continue
            linter.add_finding(
                location,
                NO_DOT_AT_END,
                number=item.content.number,
            )

    def check_2003_invalid_highnote_rise():
        for item in validated:
            current = item.content.style[0].rise
            expected = fontconfig.highnote_rise
            if equal(current, expected, MAX_HIGHNOTE_RISE_DIFF):
                continue
            linter.add_finding(
                location,
                INVALID_HIGHNOTE_RISE,
                number=item.content.number,
                current=current,
                expected=expected,
            )

    def check_2004_invalid_hignote_size():
        for item in validated:
            current = item.content.style[0].size
            expected = fontconfig.highnote_size
            if equal(current, expected, MAX_HIGHNOTE_SIZE_DIFF):
                continue
            linter.add_finding(
                location,
                INVALID_HIGHNOTE_SIZE,
                number=item.content.number,
                current=current,
                expected=expected,
            )

    def check_2005_invalid_highnote_fontfamily():
        for item in validated:
            current = item.content.style[0].font
            expected = fontconfig.highnote_fontid
            if current == expected:
                continue
            linter.add_finding(
                location,
                INVALID_HIGHNOTE_FONT_FAMILY,
                number=item.content.number,
                current=current,
                expected=expected,
            )

    def check_2010_invalid_content_fontsize():
        expected = fontconfig.content_size
        for item in validated:
            sizes = [item.size for item in item.content.style[1].content]
            sizes_equal = [
                equal(item, expected, MAX_CONTENT_SIZE_DIFF) for item in sizes
            ]
            if all(sizes_equal):
                continue
            linter.add_finding(
                location,
                INVALID_CONTENT_SIZE,
                number=item.content.number,
                current=sizes,
                expected=expected,
            )

    check_2001_no_uppercase_at_start()
    check_2002_no_dot_at_end()

    if not fontconfig:
        return

    # validation requires valid font config
    check_2005_invalid_highnote_fontfamily()
    check_2003_invalid_highnote_rise()
    check_2004_invalid_hignote_size()
    check_2010_invalid_content_fontsize()


SOLUTION = [
    protocol.Text(
        title='Die Fussnote {%number%} beginnt nicht mit einem Grossbuchstaben',
        msgid=NO_UPPERCASE_AT_START,
        description=('Ersetzen Sie den ersten Buchstaben der '
                     'Fussnote {%number%} mit einem Grossbuchstaben.'),
    ),
    protocol.Text(
        title='Die Fussnote {%number%} endet nicht mit einem Punkt',
        msgid=NO_DOT_AT_END,
        description=('Fuegen Sie einen Punkt am Ende'
                     ' der Fussnote {%number%} hinzu.'),
    ),
    # highnote/number
    protocol.Text(
        title='Fussnote {%number%}: invalid highnote rise',
        msgid=INVALID_HIGHNOTE_RISE,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
    protocol.Text(
        title='Fussnote {%number%}: invalid highnote size',
        msgid=INVALID_HIGHNOTE_SIZE,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
    protocol.Text(
        title='Fussnote {%number%}: invalid font family',
        msgid=INVALID_HIGHNOTE_FONT_FAMILY,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
    # content
    protocol.Text(
        title='Fussnote {%number%}: invalid content size',
        msgid=INVALID_CONTENT_SIZE,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
]

IDS = [
    INVALID_CONTENT_SIZE,
    INVALID_HIGHNOTE_FONT_FAMILY,
    INVALID_HIGHNOTE_RISE,
    INVALID_HIGHNOTE_SIZE,
    NO_DOT_AT_END,
    NO_UPPERCASE_AT_START,
]

STATUS = [protocol.MessageStatus(item, active=True) for item in IDS]


def equal(current, expected, max_diff: float = 0.0001):
    diff = math.fabs(expected - current)
    return diff <= max_diff
