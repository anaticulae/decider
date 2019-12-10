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


# feature existence checker
MISSING_TITLEPAGE_ID = 'E1200'

MISSING_THESIS_TYPE_ID = 'E1210'

MISSING_AUTHOR_ID = 'E1220'
MISSING_AUTHOR_MATRIKEL_ID = 'E1221'

MISSING_EXAMINER_ID = 'E1230'


def linting(titlepage: iamraw.TitlePage, linter: protocol.Linter):  # pylint:disable=too-complex

    def add_problem(msgid, location):
        linter.add_finding(
            location=location,
            msgid=msgid,
            confidence=1.0,
        )

    def check_existence():
        if titlepage is not None:
            return
        add_problem(MISSING_TITLEPAGE_ID, protocol.Location.from_page(0))

    def check_author():
        if titlepage.author:
            return
        add_problem(MISSING_AUTHOR_ID, protocol.Location.from_page(0))

    def check_author_matrikel():
        if titlepage.matrikel:
            return
        add_problem(MISSING_AUTHOR_MATRIKEL_ID, protocol.Location.from_page(0))

    def check_examiner():
        if titlepage.examiner:
            return
        add_problem(MISSING_EXAMINER_ID, protocol.Location.from_page(0))

    def check_thesis_type():
        if titlepage.thesis:
            return
        add_problem(MISSING_THESIS_TYPE_ID, protocol.Location.from_page(0))

    check_existence()

    if titlepage is None:
        # if there is no title page, the other checkers make no sence
        return

    check_author()
    check_author_matrikel()
    check_examiner()
    check_thesis_type()


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
        title='Dokument enhaelt keine Titelseite',
        msgid=MISSING_TITLEPAGE_ID,
        description=('Das Dokument enthaelt keine Titelseite. \n\n'
                     'Fuegen Sie eine Titelseite zum Dokument hinzu.'),
    ),
    create_solution(
        title='Titleseite enthaelt keinen Author',
        msgid=MISSING_AUTHOR_ID,
        description=(
            'Die Titleseite enthaellt keinen Author. \n\n'
            'Fuegen Sie ihren Namen und eventuellen akademischen Grad hinzu.'),
    ),
    create_solution(
        title='Titleseite enthaelt keine Matrikelnummer des Authors',
        msgid=MISSING_AUTHOR_MATRIKEL_ID,
        description=(
            'Die Titleseite enthaelt keine Matrikelnummer des Authors. \n\n'
            'Fuegen Sie ihre Matrikelnummer hinzu.'),
    ),
    create_solution(
        title='Titleseite enthaelt keinen Pruefer',
        msgid=MISSING_EXAMINER_ID,
        description=(
            'Die Titleseite enthaelt keinen Pruefer. \n\n'
            'Fuegen Sie die Namen und die akademischen Gerade der Pruefer auf '
            'der Titelseite hinzu.'),
    ),
    create_solution(
        title='Titleseite enthaelt keinen Thesistyp',
        msgid=MISSING_THESIS_TYPE_ID,
        description=(
            'Die Titleseite enthaelt keinen Thesistyp. \n\n'
            'Fuegen Sie den Typ(Bachelor, Master, Doktor) auf der Titelseite '
            'hinzu.'),
    ),
]

MSG_STATUS = [
    protocol.MessageStatus(
        MISSING_TITLEPAGE_ID,
        active=True,
    ),
    protocol.MessageStatus(
        MISSING_AUTHOR_ID,
        active=True,
    ),
    protocol.MessageStatus(
        MISSING_AUTHOR_MATRIKEL_ID,
        active=True,
    ),
    protocol.MessageStatus(
        MISSING_EXAMINER_ID,
        active=True,
    ),
    protocol.MessageStatus(
        MISSING_THESIS_TYPE_ID,
        active=True,
    ),
]
