# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_footnote:

Footnotes
=========
"""

import functools
import typing

import german
import iamraw
import protocol
import utila

import decider.features
import decider_footnote.footnote

DISABLE_2001_UPPER_CASE = 0.15
DISABLE_2002_DOT_END = 0.15

# minimum number of note to decide if we want to disable function. If we
# had lower numbers, judging is not possible, cause we can not determine
# if user follow this rule or not.
DISABLE_MIN_FOOTNOTE_COUNT = 15


def work(footerheader: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    headerfooters = decider_footnote.footnote.load(footerheader, pages)

    for footer in headerfooters:
        # run linter
        linting(footer, linter)

    if headerfooters:
        footnote_count = sum([len(item.content) for item in headerfooters])
    else:
        utila.info('no headerfooters')
        footnote_count = 0

    send_footnote_pattern_information(
        linter.add_finding,
        linter.result(unique=True),
        footnote_count,
    )

    result = linter.result(unique=True)

    result = judge_active(result, footnote_count)

    user, developer = protocol.dump_result(result)
    return user, developer


def linting(footer, linter: protocol.Linter):
    location = iamraw.Location.from_page(footer.page)

    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        for item in footer.content:
            checker(call, item)


SOLUTION_2001 = """\
Fußnote {{number}} beginnt nicht mit einem Großbuchstaben

Ersetzen Sie den ersten Buchstaben der Fußnote {{number}} mit einem
Großbuchstaben.

{text/fussnote#struktur}
"""

QUOTATION_SIGNS = '„‚’"”“'  # TODO: REPLACE WITH MORE GENERAL PLACE


def check_2001_no_uppercase_at_start(linter, item):
    """Ensure that footnote starts with uppercase letter.

    Quotation character before first uppercase letter are allowed.
    """
    text = item.text.strip()
    firstchar = text[0]

    if firstchar.isupper():
        return

    if firstchar.isnumeric():
        # start with number
        return

    if firstchar in QUOTATION_SIGNS:
        # start with quotation
        return

    if footnote_exception(text):
        # disable for mails and hyperlinks
        return

    linter(number=item.number)


SOLUTION_2002 = """\
Die Fußnote {{number}} endet nicht mit einem Punkt

Fügen Sie einen Punkt am Ende der Fußnote {{number}} hinzu.

{text/abkuerzung#abkurzung}
"""


def check_2002_no_dot_at_end(linter, item):
    """Ensure that footnote is closed with an dot '.'."""
    text = item.text.strip()
    lastchar = text[-1]

    if lastchar == '.':
        return

    if lastchar in QUOTATION_SIGNS and text[-2] == '.':
        # end with quotation .“
        return

    if footnote_exception(text):
        # disable for mails and hyperlinks
        return

    linter(number=item.number)


def judge_active(items, footnote_count: int):
    """Decide if some lintings are not stored, cause the user obviously
    uses an other rules than this linter checks.
    """
    if not footnote_count:
        # no footnotes, nothing to check
        return items
    disable_2001, disable_2002 = disabled(items, footnote_count)
    inactive = []
    if disable_2001:
        inactive.append(2001)
    if disable_2002:
        inactive.append(2002)
    inactive = set(inactive)  # pylint:disable=R0204
    # remove disabled messages
    result = [item for item in items if item.msgid not in inactive]
    return result


def disabled(items, footnote_count: int):
    if footnote_count < DISABLE_MIN_FOOTNOTE_COUNT:
        # disable judeging
        utila.info(f'to few footnotes({footnote_count}) to judge disabling')
        return False, False
    count_2001 = len([item.number == 2001 for item in items])
    count_2002 = len([item.number == 2002 for item in items])

    not_uppercased = utila.roundme(count_2001 / footnote_count)
    not_dotted = utila.roundme(count_2002 / footnote_count)

    utila.log(f'footnote count: {footnote_count}')
    utila.log(f'not uppercased: {not_uppercased}')  # TODO :DECREASE LOG LEVEL
    utila.log(f'not dotted: {not_dotted}')

    disable_2001 = not_uppercased > DISABLE_2001_UPPER_CASE
    disable_2002 = not_dotted > DISABLE_2002_DOT_END
    return disable_2001, disable_2002


SOLUTION_2012 = """\
Empfehlung: Anfang der Fußnote

Es wird empfohlen sämtliche Fußnoten mit einen Großbuchenstaben beginnen
zu lassen.

{text/fussnote#struktur}
"""

SOLUTION_2013 = """\
Empfehlung: Ende der Fußnote

Es wird empfohlen sämtliche Fußnoten durch einen Punkt abzuschließen.

{text/fussnote#struktur}
"""


def send_footnote_pattern_information(linter, items, footnote_count: int):
    """Send hint to user to use UpperCase/Dot pattern."""
    disable_2001, disable_2002 = disabled(items, footnote_count)
    # TODO: USE LINTER INFORMATION TYPE
    if disable_2001:
        linter(
            msgid=2012,
            location=decider.features.OVERVIEW,
        )
    if disable_2002:
        linter(
            msgid=2013,
            location=decider.features.OVERVIEW,
        )


# To ignore dots, spaces or <>.
MAX_FOOTENOTE_EXCEPTION_CHARS = 10


def footnote_exception(text: str) -> bool:
    """Skip dot checking and upper cases for emails and hyperlinks. See:
    <Theissen:2017>.

    >>> footnote_exception('1<helmut.k.fahrendholz@mailbox.tu-berlin.de>123')
    True
    >>> footnote_exception('<http://www.url.com>123.')
    True
    >>> footnote_exception('This is a hyperlink: <http://www.url.com>.')
    False
    """
    text = text.strip()
    if not text:
        return False
    parsed = german.hyperlink(text) + german.mails(text)  # pylint:disable=E1101
    detected = ''.join(parsed)
    diff = len(text) - len(detected)
    assert diff >= 0, str(diff)
    return diff <= MAX_FOOTENOTE_EXCEPTION_CHARS
