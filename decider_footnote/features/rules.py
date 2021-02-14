# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_footnote:

Footnotes
=========
"""

import protocol
import serializeraw
import utila

import decider_footnote.rules.start


def work(
        footerheader: str,
        horizontals: str,
        pages: tuple = None,
) -> protocol.ResultType:
    # load data
    footnotes = serializeraw.load_footnotes(footerheader, pages)
    # TODO: REPLACE WITH utila.flatten_content
    footnotes_flat = utila.flatten([item.content for item in footnotes])
    horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    driver = protocol.driver(
        footnotes=footnotes_flat,
        footnotes_pages=footnotes,
        horizontals=horizontals,
    )
    # run linting
    result = protocol.run(__name__, driver=driver, before_dump=before_dump)
    return result


def before_dump(result, driver, linter):
    footnote_count = len(driver.footnotes)
    if not footnote_count:
        utila.info('no headerfooters')
    else:
        decider_footnote.rules.start.send_footnote_pattern_information(
            linter.add_finding,
            result,
            footnote_count,
        )
        result = linter.result()
    result = decider_footnote.rules.start.judge_active(result, footnote_count)
    return result


SOLUTION_2001 = """\
Fußnote {{number}} beginnt nicht mit einem Großbuchstaben

Ersetzen Sie den ersten Buchstaben der Fußnote {{number}} mit einem \
Großbuchstaben.

{text/fussnote#struktur}
"""

QUOTATION_SIGNS = '„‚’"”“'  # TODO: REPLACE WITH MORE GENERAL PLACE


def check_2001_no_uppercase_at_start(linter, driver):
    """Ensure that footnote starts with uppercase letter.

    Quotation character before first uppercase letter are allowed.
    """
    for footnote in driver.footnotes:
        text = footnote.text.strip()
        firstchar = text[0]

        if firstchar.isupper():
            continue
        if firstchar.isnumeric():
            # start with number
            continue
        if firstchar in QUOTATION_SIGNS:
            # start with quotation
            continue
        if decider_footnote.rules.start.footnote_exception(text):
            # disable for mails and hyperlinks
            continue
        linter(number=footnote.number)


SOLUTION_2002 = """\
Die Fußnote {{number}} endet nicht mit einem Punkt

Fügen Sie einen Punkt am Ende der Fußnote {{number}} hinzu.

{text/abkuerzung#abkurzung}
"""


def check_2002_no_dot_at_end(linter, driver):
    """Ensure that footnote is closed with an dot '.'."""
    for footnote in driver.footnotes:
        text = footnote.text.strip()
        lastchar = text[-1]

        if lastchar == '.':
            continue
        if lastchar in QUOTATION_SIGNS and text[-2] == '.':
            # end with quotation .“
            continue
        if decider_footnote.rules.start.footnote_exception(text):
            # disable for mails and hyperlinks
            continue
        linter(number=footnote.number)


SOLUTION_2012 = """\
Empfehlung: Anfang der Fußnote

Es wird empfohlen sämtliche Fußnoten mit einen Großbuchenstaben beginnen \
zu lassen.

{text/fussnote#struktur}
"""

SOLUTION_2013 = """\
Empfehlung: Ende der Fußnote

Es wird empfohlen sämtliche Fußnoten durch einen Punkt abzuschließen.

{text/fussnote#struktur}
"""

SOLUTION_R2017 = """\
Quellenangabe uneindeutig

Vermeiden Sie **Ebd.** am Anfang der Fußnoten auf einer neuen Seite \
(Fußnote: {{number}}).

Empfehlung: Komplette Quellenangabe am Seitenanfang um auch bei einzeln \
kopierten Seiten komplette Quellenangaben zu erhalten.

{text/fussnote#struktur}
"""


def check_2017_ambiguous_reference(linter, driver):
    for page in driver.footnotes_pages:
        content = page.content
        first = content[0].text.lower()
        if not 'ebd.' in first:
            continue
        linter(number=content[0].number)


SOLUTION_R2018 = """\
Fußnote verstreut

Vermeiden Sie die Fußnoten über mehrere Seiten zu verteilen.

# TODO: IF WORD, ADD LINK TO ARTICLE

{text/fussnote#struktur}
"""


def check_2018_footnote_over_pages(linter, driver):
    for page in driver.footnotes_pages:
        content = page.content
        first = content[0]
        if first.number != -1:
            # TODO: HOW TO DECIDE BETWEEN PARSING ERROR
            # TODO: IMPROVE THIS CHECK
            continue
        linter()


SOLUTION_R2019 = """\
Fußnote dupliziert, vermeiden Sie Redundanz

Identisch, aufeinander folgende Fußnoten erkannt. Verwenden Sie **ebd. \
order ???** um identische Fußnoten darzustellen.

{text/fussnote#struktur}
"""


def check_2019_duplicated_footnote(linter, driver):
    for footnotes_pages in driver.footnotes_pages:
        footnotes_pages = footnotes_pages.content
        for current, after in zip(footnotes_pages[:-1], footnotes_pages[1:]):
            if current.text.strip() != after.text.strip():
                continue
            linter()
