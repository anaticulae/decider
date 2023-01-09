# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_titlepage:

Titlepage
=========
"""

import iamraw
import protocol
import serializeraw
import utila


def work(titles: str) -> tuple[str, str]:
    driver = create_driver(titlepage=titles)
    location = 0
    if driver.titlepage:  # pylint:disable=E1101
        location = utila.ifnone(driver.titlepage.pageraw, default=0)  # pylint:disable=E1101
    result = protocol.run(
        modulename=__name__,
        driver=driver,
        location=iamraw.Location.from_page(location),
    )
    return result


def create_driver(titlepage: str):
    if utila.exists(titlepage):
        titlepage: iamraw.TitlePage = serializeraw.load_titlepage(titlepage)
    else:
        titlepage = None
    return protocol.driver(titlepage=titlepage)


SOLUTION_E1200 = """\
Dokument enthält keine Titelseite

Fügen Sie eine Titelseite zum Dokument hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1200_titlepage_existence(linter, driver):
    if driver.titlepage:
        return
    linter(location=protocol.OVERVIEW)


SOLUTION_E1220 = """\
Titelseite enthält keinen Autor

Fügen Sie ihren Namen und eventuellen akademischen Grad auf \
der Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1220_author_existence(linter, driver):
    if not driver.titlepage:
        return
    if driver.titlepage.author:
        return
    linter()


SOLUTION_E1221 = """\
Titelseite enthält keine Matrikelnummer

Fügen Sie ihre Matrikelnummer auf der Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1221_author_matrikel_existence(linter, driver):
    if not driver.titlepage:
        return
    if driver.titlepage.matrikel:
        return
    linter()


SOLUTION_E1230 = """\
Titelseite enthält keinen Prüfer

Fügen Sie die Namen und die akademischen Grade der Prüfer auf der \
Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1230_author_matrikel_existence(linter, driver):
    if not driver.titlepage:
        return
    if driver.titlepage.examiner:
        return
    linter()


SOLUTION_E1210 = """\
Titelseite enthält keinen Thesistyp

Fügen Sie den Typ(Studienarbeit, Bachelorarbeit, Masterarbeit, \
Doktorarbeit oder Dissertation) auf der Titelseite hinzu.

{elemente/titelblatt#zwingend-notwendige-angaben}
"""


def check_1210_thesis_type_existence(linter, driver):
    if not driver.titlepage:
        return
    if driver.titlepage.thesis:
        return
    linter()


SOLUTION_1211 = """\
Seitenzahl auf Titelblatt

Das Titelblatt einhält eine Seitenzahl: **{{pagenumber}}**.
 Es wird empfohlen keine Seitenzahl auf dem Titelblatt anzugeben.

{elemente/titelblatt}
"""


def check_1211_titlepage_no_pagenumber(linter, driver):
    if not driver.titlepage:
        return
    try:
        pagenumber = driver.titlepage.pagenumber
    except AttributeError:
        # TODO: REMOVE AFTER UPGRADING IAMRAW
        pagenumber = None
    if not pagenumber:
        return
    linter(pagenumber=pagenumber)
