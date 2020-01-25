# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import typing

import protocol
import yaml

import decider.footnotes


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = create_linter()

    headerfooters = decider.footnotes.load(footerheader, pages)
    for footer in headerfooters:
        footnotes = [
            decider.footnotes.validate(item) for item in footer.content
        ]
        # run linter
        linting(footnotes, footer.page, linter)

    result = linter.result(unique=True)

    # dump linter result
    user_dumped = yaml.dump(result[0])
    developer_dumped = yaml.dump(result[1])
    return user_dumped, developer_dumped


# TODO: ADD GENERAL PACKAGE TO DEFINE UNIQUE IDS
FOOTER_CHECKER_ID = 20

NO_UPPERCASE_AT_START = 2001
NO_DOT_AT_END = 2002


def linting(validated, page: int, linter: protocol.Linter):

    def add_problem(msgid, location, number):
        linter.add_finding(
            location=location,
            msgid=msgid,
            confidence=1.0,
            number=number,
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

    check_start()
    check_end()


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
]

MSG_STATUS = [
    protocol.MessageStatus(
        item,
        active=True,
    ) for item in [
        NO_DOT_AT_END,
        NO_UPPERCASE_AT_START,
    ]
]
