# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_titlepage:

Titlepage
=========
"""
import functools
import typing

import iamraw
import protocol
import serializeraw
import yaml

import decider.utils

TITLEPAGE_CHECKER_ID = 12


def work(titlepage_path: str) -> typing.Tuple[str, str]:
    linter = decider.utils.from_module(__name__)

    titlepage: iamraw.TitlePage = serializeraw.load_titlepage(titlepage_path)

    # run linter
    linting(titlepage, linter)

    result = linter.result(unique=True)

    # dump linter result
    user_dumped = yaml.dump(result[0])
    developer_dumped = yaml.dump(result[1])
    return user_dumped, developer_dumped


def linting(
        titlepage: iamraw.TitlePage,
        linter: protocol.Linter,
):
    location = protocol.Location.from_page(0)
    checkers = decider.utils.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, titlepage)


SOLUTION_1200 = """\
Dokument enhaelt keine Titelseite

Fuegen Sie eine Titelseite zum Dokument hinzu.
"""


def check_1200_titlepage_existence(linter, titlepage):
    if titlepage is not None:
        return
    linter()


SOLUTION_1220 = """\
Titleseite enthaelt keinen Author

Fuegen Sie ihren Namen und eventuellen akademischen Grad hinzu.
"""


def check_1220_author_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.author:
        return
    linter()


SOLUTION_1221 = """\
Titleseite enthaelt keine Matrikelnummer des Authors

Fuegen Sie ihre Matrikelnummer hinzu.
"""


def check_1221_author_matrikel_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.matrikel:
        return
    linter()


SOLUTION_1230 = """\
Titleseite enthaelt keinen Pruefer

Fuegen Sie die Namen und die akademischen Gerade der Pruefer auf der
Titelseite hinzu.
"""


def check_1230_author_matrikel_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.examiner:
        return
    linter()


SOLUTION_1210 = """\
Die Titleseite enthaelt keinen Thesistyp

Fuegen Sie den Typ(Bachelor, Master, Doktor) auf der Titelseite hinzu.
"""


def check_1210_thesis_type_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.thesis:
        return
    linter()
