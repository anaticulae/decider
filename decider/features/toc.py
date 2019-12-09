# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol


def work() -> str:
    pass


TITLEPAGE_CHECKER_ID = 13

MISSING_TOC_ID = 1300


def linting(toc: iamraw.Toc, linter: protocol.Linter):  # pylint:disable=too-complex

    def add_problem(msgid, location):
        linter.add_finding(
            location=location,
            msgid=msgid,
            confidence=1.0,
        )

    def check_existence():
        if toc.children:
            return
        add_problem(MISSING_TOC_ID, protocol.Location.frompage(0))

    check_existence()
    if not toc.children:
        return


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
        title='Dokument enhaelt kein Inhaltsverzeichnis',
        msgid=MISSING_TOC_ID,
        description=('Das Dokument enthaelt kein Inhaltsverzeichnis. \n\n'
                     'Fuegen Sie ein Inhaltsverzeichnis zum Dokument hinzu.'),
    ),
]

MSG_STATUS = [
    protocol.MessageStatus(
        MISSING_TOC_ID,
        active=True,
    ),
]
