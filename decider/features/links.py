# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Decider Links
=============

10500: date of hyperlink access
"""

import configo
import german
import iamraw
import protocol
import serializeraw
import utila

import decider.links.date
import decider.links.validate


def work(
    biblio: str,
    footer: str,
    sentence: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = create_driver(
        biblio,
        footer,
        sentence,
        pages=pages,
    )
    dumped = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return dumped


def create_driver(biblio: str, footer: str, sentence: str, pages: tuple = None):
    hyperlinks = []
    for path in (biblio, footer, sentence):
        if not utila.exists(path):
            utila.error(f'missing: {path}')
            continue
        loaded = serializeraw.load_hyperlinks(
            path,
            pages=pages,
        )
        hyperlinks.extend(loaded)
    result = protocol.driver(hyperlinks=hyperlinks)
    return result


SOLUTION_E10500 = """\
Aufrufdatum fehlt

Für den Hyperlink **{{link.href|wordwrap(40)}}** ist kein Aufrufdatum angegeben.

{darstellung/hyperlink}
"""

PARAGRAPH_TOO_SHORT = configo.HV_INT_PLUS(default=3)


def check_10500_hyperlink_require_date(linter: callable, driver):
    """Check that Hyperlink has access label."""
    hyperlinks = driver.hyperlinks
    for link in hyperlinks:
        if link.visited:
            continue
        location = iamraw.Location.from_page(link.page)
        linter(location=location, link=link)


SOLUTION_E10510 = """\
Hyperlink nicht erreichbar

Auf den Hyperlink **{{link.href|wordwrap(40)}}** kann nicht zugegriffen \
werden. Überprüfen Sie die Schreibweise bzw. achten Sie darauf dass der \
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


SOLUTION_E10515 = """\
Hyperlink verweist auf lokale Datei

Der Hyperlink **{{link.href|wordwrap(40)}}** verweist of die lokale
Festplatte.
"""


def check_10515_hyperlink_local(linter: callable, driver):
    for hyperlink in driver.hyperlinks:
        if not german.locallink(hyperlink.href):
            continue
        location = iamraw.Location.from_page(hyperlink.page)
        linter(link=hyperlink, location=location)


SOLUTION_W10520 = """\
Uneindeutige Zugriffsdaten erkannt

Um Missverständnisse zu vermeiden verwenden Sie ein eindeutiges Datum im \
Format:

YYYY.MM.DD oder DD.MM.YYYY.

{darstellung/schreibweise#datum-und-uhrzeit}
{darstellung/hyperlink}
TODO: Add Dates link
"""


def check_10520_hyperlink_mixed_date_exists(linter: callable, driver):
    dates = [item.visited for item in driver.hyperlinks if item.visited]
    if not decider.links.date.is_mixed(dates):
        return
    linter(location=protocol.OVERVIEW)


SOLUTION_W6016 = """\
Uneindeutige Datum erkannt

Jahreszahl **{{date}}** weicht vom erkannten Datums-Standard ab.

{darstellung/schreibweise#datum-und-uhrzeit}
{darstellung/hyperlink}
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
