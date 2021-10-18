# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import inspect
import typing

import configo
import iamraw
import protocol
import serializeraw
import utila

import decider_footnote.footnote

HIGHNOTE_RISE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=0.5)

HIGHNOTE_SIZE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=0.5)

CONTENT_SIZE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=0.5)

# as a result of bad layout extraction
RISE_NOISE_MAX = configo.HV_FLOAT_PLUS(default=2.0)


def work(
    footerheader: str,
    fontheader: str,
    fontcontent: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    headerfooters = serializeraw.load_footnotes(footerheader, pages)
    footnotes = utila.flatten([item.content for item in headerfooters if item])
    fontconfig = decider_footnote.footnote.most_common_font(footnotes)

    fontstore = serializeraw.create_fontstore(fontheader, fontcontent)

    for footer in headerfooters:
        # run linter for every page
        linting(footer, fontconfig, fontstore, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
    footer,
    fontconfig: decider_footnote.footnote.FootNoteStyle,
    fontstore: iamraw.FontStore,
    linter: protocol.Linter,
):
    location = iamraw.Location.from_page(footer.page)

    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        for item in footer.content:
            datum = protocol.driver(
                item=item,
                fontconfig=fontconfig,
                fontstore=fontstore,
            )
            checker(call, datum)


SOLUTION_2003 = """\
Fußnote {{number}} falsch formatiert

Die Schriftgröße der Fußnotenummer **{{current}}** weicht von der \
erwarteten Schriftgröße der Fußnotennummer **{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2003_invalid_highnote_rise(linter, driver):
    """Ensure that footnote fits to `common` footnote highnote numer rise."""
    item = driver.item
    if not item.style:
        return
    current = item.style[0].rise
    expected = driver.fontconfig.highnote_rise

    if isinstance(expected, list):
        skip_method(f'ambiguous expected highnote rise: {expected}')
        return
    if utila.near(current, expected, HIGHNOTE_RISE_DIFF_MAX):
        return

    linter(number=item.number, current=current, expected=expected)


SOLUTION_2004 = """\
Fußnote {{number}} falsch formatiert

Die Schriftgröße **{{current}}** weicht von der erwarteten Schriftgröße \
**{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2004_invalid_hignote_size(linter, driver):
    """Ensure correct font size of highnote."""
    item = driver.item
    if not item.style:
        return
    current = item.style[0].size
    expected = driver.fontconfig.highnote_size

    if isinstance(expected, list):
        skip_method(f'ambiguous expected highnote size: {expected}')
        return
    if utila.near(current, expected, HIGHNOTE_SIZE_DIFF_MAX):
        return

    linter(number=item.number, current=current, expected=expected)


SOLUTION_2005 = """\
Fußnote {{number}} falsch formatiert

Die Schriftart **{{current}}** weicht von der erwarteten Schriftart \
**{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2005_invalid_highnote_fontfamily(linter, driver):
    """Ensure correct font family of highnote."""
    item = driver.item
    if not item.style:
        return
    current = item.style[0].font
    expected = driver.fontconfig.highnote_fontid

    if isinstance(expected, list):
        skip_method(f'ambiguous expected highnote fontfamily: {expected}')
        return

    current = driver.fontstore[current]
    expected = driver.fontstore[expected]

    if not current or not expected:
        skip_method('missing font, regenerate resources')
        return

    current = current.name.lower()
    expected = expected.name.lower()

    if current == expected:
        return

    linter(number=item.number, current=current, expected=expected)


SOLUTION_2010 = """\
Fußnote {{number}} falsch formatiert

Die Schriftgröße **{{current}}** weicht von der erwarteten Schriftgröße \
**{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2010_invalid_content_fontsize(linter, driver):
    """Ensure correct font size of footnote content."""
    item = driver.item
    expected = driver.fontconfig.content_size

    if isinstance(expected, list):
        skip_method(f'ambiguous expected highnote fontsize: {expected}')
        return
    if not item.style:
        skip_method('missing style')
        return
    text = item.text
    footnotestyle = item.style[1]

    # The style of the last footnote includes the ending
    # whitespace/newline. This whitespace is formatted as next text token.
    # This is a result of requirements. The next token is the page number
    # with may differ in font size. Therefore we only validate text
    # positions which are characters.
    # do not check on whitespace or newline
    footnotestyle = [
        item for item in footnotestyle if text[item.start:item.end].strip()
    ]
    # not not check highnotes inside footnote
    sizes = [item.size for item in footnotestyle if item.rise < RISE_NOISE_MAX]

    sizes_equal = [
        utila.near(item, expected, CONTENT_SIZE_DIFF_MAX) for item in sizes
    ]
    if all(sizes_equal):
        return

    linter(number=item.number, current=sizes, expected=expected)


def skip_method(msg: str = ''):
    # TODO: MOVE TO UTILA
    frame = inspect.currentframe()
    caller = [item.function for item in inspect.getouterframes(frame)[0:5]]
    caller = [item for item in caller if 'check_' in item]
    caller = ' '.join(caller)
    utila.error(msg)
    utila.error(f'skip: {caller}')
