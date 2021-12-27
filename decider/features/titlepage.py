# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
import utila


def work(titlepage_path: str) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    titlepage: iamraw.TitlePage = serializeraw.load_titlepage(titlepage_path)

    # run linter
    linting(titlepage, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result, unique=True)

    return user, developer


def linting(
    titlepage: iamraw.TitlePage,
    linter: protocol.Linter,
):
    pdflocation = utila.ifnone(titlepage.pageraw, default=0) if titlepage else 0
    location = iamraw.Location.from_page(pdflocation)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, titlepage)


SOLUTION_E1200 = """\
Dokument enthält keine Titelseite

Fügen Sie eine Titelseite zum Dokument hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1200_titlepage_existence(linter, titlepage):
    if titlepage is not None:
        return
    linter(location=protocol.OVERVIEW)


SOLUTION_E1220 = """\
Titelseite enthält keinen Autor

Fügen Sie ihren Namen und eventuellen akademischen Grad auf \
der Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1220_author_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.author:
        return
    linter()


SOLUTION_E1221 = """\
Titelseite enthält keine Matrikelnummer

Fügen Sie ihre Matrikelnummer auf der Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1221_author_matrikel_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.matrikel:
        return
    linter()


SOLUTION_E1230 = """\
Titelseite enthält keinen Prüfer

Fügen Sie die Namen und die akademischen Grade der Prüfer auf der \
Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1230_author_matrikel_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.examiner:
        return
    linter()


SOLUTION_E1210 = """\
Titelseite enthält keinen Thesistyp

Fügen Sie den Typ(Studienarbeit, Bachelorarbeit, Masterarbeit, \
Doktorarbeit oder Dissertation) auf der Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1210_thesis_type_existence(linter, titlepage):
    if titlepage is None:
        return
    if titlepage.thesis:
        return
    linter()
