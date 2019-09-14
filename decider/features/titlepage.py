# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import protocol
import serializeraw
import yaml

TITLEPAGE_CHECKER_ID = 12


def work(titlepage_path: str) -> typing.Tuple[str, str]:
    linter = create_linter()

    titlepage: iamraw.TitlePage = serializeraw.load_titlepage(titlepage_path)
    assert titlepage, str(titlepage)

    # run linter
    linting(titlepage, linter)

    result = linter.result(unique=True)

    # dump linter result
    user_dumped = yaml.dump(result[0])
    developer_dumped = yaml.dump(result[1])
    return user_dumped, developer_dumped


def create_linter() -> protocol.Linter:
    solver = protocol.Solver()
    for item in SOLUTION:
        solver.add_solution(item.msgid, item)

    linter = protocol.Linter(
        active=MSG_STATUS,
        solver=solver,
    )
    return linter


MISSING_AUTHOR_ID = 'E1200'


def linting(titlepage: iamraw.TitlePage, linter: protocol.Linter):

    def check_author():
        if titlepage.author:
            return
        linter.add_finding(
            location=protocol.Location.fromstr('p0'),
            msgid=MISSING_AUTHOR_ID,
            confidence=1.0,
        )

    check_author()


SOLUTION = [
    protocol.Text(
        title='Titleseite enthaellt keinen Author',
        description=(
            'Die Titleseite enthaelt keinen Author. \n\n'
            'Fuegen Sie ihren Namen und eventuellen akademischen Grad hinzu.'),
        status=protocol.ProblemStatus.OPEN,
        msgid=MISSING_AUTHOR_ID,
    ),
]

MSG_STATUS = [
    protocol.MessageStatus(
        MISSING_AUTHOR_ID,
        active=True,
    ),
]
