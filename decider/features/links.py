# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Decider Links
=============

10500: date of hyperlink access
"""

import typing

import iamraw
import protocol
import serializeraw
import utila

import decider
import decider.links.date
import decider.links.validate


def work(links: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)
    # load data
    hyperlinks = serializeraw.load_hyperlinks(links, pages=pages)  # pylint:disable=E1101
    driver = protocol.driver(hyperlinks=hyperlinks)

    # run linter
    linter.run(driver=driver)

    # write result
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_10500 = """\
Aufrufdatum fehlt

Für den Hyperlink **{{link.href|wordwrap(40)}}** ist kein Aufrufdatum angegeben.

{darstellung/hyperlink}
"""

PARAGRAPH_TOO_SHORT = 3


def check_10500_hyperlink_require_date(linter: callable, driver):
    """Check that Hyperlink has access label."""
    hyperlinks = driver.hyperlinks
    for link in hyperlinks:
        if link.visited:
            continue
        location = iamraw.Location.from_page(link.page)
        linter(location=location, link=link)


SOLUTION_10510 = """\
Hyperlink nicht erreichbar

Auf den Hyperlink **{{link.href|wordwrap(40)}}** kann nicht zugegriffen
werden. Überprüfen Sie die Schreibweise bzw. achten Sie darauf dass der
Hyerplink ohne weitere Authorisierung erreichbar ist.

{darstellung/hyperlink}
"""


def check_10510_hyperlink_existence(linter: callable, driver):
    hyperlinks = [item.href for item in driver.hyperlinks]

    result = decider.links.validate.visit(hyperlinks)
    if not result:
        # validation error
        return

    for hyperlink, validated in zip(driver.hyperlinks, result):
        validated = validated.split()[0]
        if validated == 'True':
            continue
        location = iamraw.Location.from_page(hyperlink.page)
        linter(location=location, link=hyperlink)


SOLUTION_10520 = """\
Uneindeutige Zugriffsdaten erkannt

Um Missverständnisse zu vermeiden verwenden Sie ein eindeutiges Datum im Format:

YYYY.MM.DD oder DD.MM.YYYY.

{darstellung/hyperlink}
TODO: Add Dates link
"""


def check_10520_hyperlink_mixed_date_exists(linter: callable, driver):
    dates = [item.visited for item in driver.hyperlinks if item.visited]
    if not decider.links.date.is_mixed(dates):
        return
    linter(location=decider.features.OVERVIEW)


SOLUTION_6016 = """\
Uneindeutige Datum erkannt

Jahreszahl **{{date}}** weicht vom erkannten Datums-Standard ab.

{darstellung/hyperlink}
TODO: Add Dates link
"""


def check_10521_hyperlink_mixed_access_date(linter: callable, driver):
    dates = [item.visited for item in driver.hyperlinks if item.visited]
    if decider.links.date.is_mixed(dates):
        # message 10520 is used to inform user aboud changing
        # dates-format. We avoid to highlight a lot of `wrong` dates,
        # cause using other dates format.
        return
    for hyperlink in driver.hyperlinks:
        if not hyperlink.visited:
            continue
        if not decider.links.date.mixed(hyperlink.visited):
            continue
        location = iamraw.Location.from_page(hyperlink.page)
        linter(
            date=utila.from_tuple(hyperlink.visited, separator='.'),
            location=location,
        )
