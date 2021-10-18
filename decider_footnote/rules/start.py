# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import protocol
import utila

DISABLE_2001_UPPER_CASE = 0.15
DISABLE_2002_DOT_END = 0.15

# minimum number of note to decide if we want to disable function. If we
# had lower numbers, judging is not possible, cause we can not determine
# if user follow this rule or not.
DISABLE_FOOTNOTE_COUNT_MIN = 15

# To ignore dots, spaces or <>.
FOOTENOTE_EXCEPTION_CHARS_MAX = 10


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


def send_footnote_pattern_information(linter, items, footnote_count: int):
    """Send hint to user to use UpperCase/Dot pattern."""
    disable_2001, disable_2002 = disabled(items, footnote_count)
    # TODO: USE LINTER INFORMATION TYPE
    if disable_2001:
        linter(
            msgid=2012,
            location=protocol.OVERVIEW,
        )
    if disable_2002:
        linter(
            msgid=2013,
            location=protocol.OVERVIEW,
        )


def disabled(items, footnote_count: int):
    if footnote_count < DISABLE_FOOTNOTE_COUNT_MIN:
        # disable judeging
        utila.info(f'to few footnotes({footnote_count}) to judge disabling')
        return False, False
    count_2001 = protocol.count_findings(items, 2001)
    count_2002 = protocol.count_findings(items, 2002)

    not_uppercased = utila.roundme(count_2001 / footnote_count)
    not_dotted = utila.roundme(count_2002 / footnote_count)

    utila.log(f'footnote count: {footnote_count}')
    utila.log(f'not uppercased: {not_uppercased}')  # TODO :DECREASE LOG LEVEL
    utila.log(f'not dotted: {not_dotted}')

    disable_2001 = not_uppercased > DISABLE_2001_UPPER_CASE
    disable_2002 = not_dotted > DISABLE_2002_DOT_END
    return disable_2001, disable_2002


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
    return diff <= FOOTENOTE_EXCEPTION_CHARS_MAX
