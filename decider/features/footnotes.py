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
import yaml

import decider.footnotes

MAX_HIGHNOTE_RISE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value
MAX_HIGHNOTE_SIZE_DIFF = configo.HV_FLOAT_PLUS(default=0.5).value


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = create_linter()

    headerfooters = decider.footnotes.load(footerheader, pages)
    footnotes = utila.flatten([item.content for item in headerfooters if item])
    fontconfig = decider.footnotes.most_common_font(footnotes)
    for footer in headerfooters:
        footnotes = [
            decider.footnotes.validate(item) for item in footer.content
        ]
        # run linter
        linting(footnotes, fontconfig, footer.page, linter)

    result = linter.result(unique=True)

    # dump linter result
    user_dumped = yaml.dump(result[0])
    developer_dumped = yaml.dump(result[1])
    return user_dumped, developer_dumped


# TODO: ADD GENERAL PACKAGE TO DEFINE UNIQUE IDS
FOOTER_CHECKER_ID = 20

NO_UPPERCASE_AT_START = 2001
NO_DOT_AT_END = 2002
INVALID_HIGHNOTE_RISE = 2003
INVALID_HIGHNOTE_SIZE = 2004
INVALID_HIGHNOTE_FONT_FAMILY = 2005


def linting(
        validated,
        fontconfig: decider.footnotes.FootNoteStyle,
        page: int,
        linter: protocol.Linter,
):

    def add_problem(msgid, location, number, **kwargs):
        linter.add_finding(
            location=location,
            msgid=msgid,
            confidence=1.0,
            number=number,
            **kwargs,
        )

    location = protocol.Location.from_page(page)

    def check_start():
        # item : decider.footnotes.Validated
        for item in validated:
            if item.uppercase:
                continue
            add_problem(
                NO_UPPERCASE_AT_START,
                location,
                number=item.content.number,
            )

    def check_end():
        # item : decider.footnotes.Validated
        for item in validated:
            if item.ends:
                continue
            add_problem(
                NO_DOT_AT_END,
                location,
                number=item.content.number,
            )

    def check_highnote_rise():
        for item in validated:
            current = item.content.style[0].rise
            expected = fontconfig.highnote_rise
            if equal(current, expected, MAX_HIGHNOTE_RISE_DIFF):
                continue
            add_problem(
                INVALID_HIGHNOTE_RISE,
                location,
                number=item.content.number,
                current=current,
                expected=expected,
            )

    def check_highnote_size():
        for item in validated:
            current = item.content.style[0].size
            expected = fontconfig.highnote_size
            if equal(current, expected, MAX_HIGHNOTE_SIZE_DIFF):
                continue
            add_problem(
                INVALID_HIGHNOTE_SIZE,
                location,
                number=item.content.number,
                current=current,
                expected=expected,
            )

    def check_highnote_font_family():
        for item in validated:
            current = item.content.style[0].font
            expected = fontconfig.highnote_fontid
            if current == expected:
                continue
            add_problem(
                INVALID_HIGHNOTE_FONT_FAMILY,
                location,
                number=item.content.number,
                current=current,
                expected=expected,
            )

    check_start()
    check_end()

    if not fontconfig:
        return

    # validation requires valid font config
    check_highnote_font_family()
    check_highnote_rise()
    check_highnote_size()


def create_linter() -> protocol.Linter:
    solver = protocol.Solver()
    for item in SOLUTION:
        solver.add_solution(item.msgid, item)

    linter = protocol.Linter(
        active=MSG_STATUS,
        solver=solver,
    )
    return linter


def create_solution(title: str, msgid: str, description: str):
    result = protocol.Text(
        title=title,
        description=description,
        status=protocol.ProblemStatus.OPEN,
        msgid=msgid,
    )
    return result


SOLUTION = [
    create_solution(
        title='Die Fussnote {%number%} beginnt nicht mit einem Grossbuchstaben',
        msgid=NO_UPPERCASE_AT_START,
        description=('Ersetzen Sie den ersten Buchstaben der '
                     'Fussnote {%number%} mit einem Grossbuchstaben.'),
    ),
    create_solution(
        title='Die Fussnote {%number%} endet nicht mit einem Punkt',
        msgid=NO_DOT_AT_END,
        description=('Fuegen Sie einen Punkt am Ende'
                     ' der Fussnote {%number%} hinzu.'),
    ),
    create_solution(
        title='Fussnote {%number%}: invalid highnote rise',
        msgid=INVALID_HIGHNOTE_RISE,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
    create_solution(
        title='Fussnote {%number%}: invalid highnote size',
        msgid=INVALID_HIGHNOTE_SIZE,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
    create_solution(
        title='Fussnote {%number%}: invalid font family',
        msgid=INVALID_HIGHNOTE_FONT_FAMILY,
        description='Expected: {%expected%} != Current: {%current%}',
    ),
]

IDS = [
    INVALID_HIGHNOTE_FONT_FAMILY,
    INVALID_HIGHNOTE_RISE,
    INVALID_HIGHNOTE_SIZE,
    NO_DOT_AT_END,
    NO_UPPERCASE_AT_START,
]

MSG_STATUS = [protocol.MessageStatus(item, active=True) for item in IDS]


def equal(current, expected, max_diff: float = 0.0001):
    diff = math.fabs(expected - current)
    return diff <= max_diff
