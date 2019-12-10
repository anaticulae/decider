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

import decider.toc.level as dtl


def work(tableofcontent: str) -> typing.Tuple[str, str]:
    linter = create_linter()

    tableofcontent: iamraw.Toc = serializeraw.load_toc(tableofcontent)

    # run linter
    linting(tableofcontent, linter)

    result = linter.result(unique=False)

    # dump linter result
    user_dumped = yaml.dump(result[0])
    developer_dumped = yaml.dump(result[1])
    return user_dumped, developer_dumped


TITLEPAGE_CHECKER_ID = 13

MISSING_TOC_ID = 1300

SINGLE_CHILDREN_ID = 1350
LEVEL_TOO_DEEP_ID = 1351


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
        add_problem(MISSING_TOC_ID, protocol.Location.from_page(0))

    check_existence()
    if not toc.children:
        return

    level_result: dtl.TocValidationResult = dtl.validate(toc)

    def check_level():
        for _ in level_result.level_to_deep:  # pylint:disable=E1133
            add_problem(LEVEL_TOO_DEEP_ID, protocol.Location.from_page(1))

    def check_children():
        for _ in level_result.too_few_children:  # pylint:disable=E1133
            add_problem(SINGLE_CHILDREN_ID, protocol.Location.from_page(1))

    check_level()
    check_children()


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
        item,
        active=True,
    ) for item in [
        LEVEL_TOO_DEEP_ID,
        MISSING_TOC_ID,
        SINGLE_CHILDREN_ID,
    ]
]
