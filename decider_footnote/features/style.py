# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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

skip = protocol.skip_method  # pylint:disable=C0103


def work(
    footerheader: str,
    fontheader: str,
    fontcontent: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = create_driver(
        headerfooters=footerheader,
        fontheader=fontheader,
        fontcontent=fontcontent,
        pages=pages,
    )
    result = protocol.run(
        __name__,
        driver=driver,
    )
    return result


def create_driver(
    headerfooters: str,
    fontheader: str,
    fontcontent: str,
    pages: tuple = None,
):
    headerfooters = serializeraw.load_footnotes(
        headerfooters,
        pages=pages,
    )
    footnotes = utila.flatten([item.content for item in headerfooters if item])
    fontconfig = decider_footnote.footnote.most_common_font(footnotes)
    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    result = protocol.driver(
        footnotes=footnotes,
        fontconfig=fontconfig,
        fontstore=fontstore,
    )
    return result


SOLUTION_2003 = """\
Fußnote {{number}} falsch formatiert

Die Schriftgröße der Fußnotenummer **{{current}}** weicht von der \
erwarteten Schriftgröße der Fußnotennummer **{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2003_invalid_highnote_rise(linter, driver):
    """Ensure that footnote fits to `common` footnote highnote numer rise."""
    for footnote in driver.footnotes:
        if not footnote.style_number:
            continue
        current = footnote.style_number.rise
        expected = driver.fontconfig.highnote_rise
        if isinstance(expected, list):
            skip(f'ambiguous expected highnote rise: {expected}')
            continue
        if utila.near(current, expected, HIGHNOTE_RISE_DIFF_MAX):
            continue
        linter(
            number=footnote.number,
            current=current,
            expected=expected,
            location=iamraw.Location.from_page(footnote.page),
        )


SOLUTION_2004 = """\
Fußnote {{number}} falsch formatiert

Die Schriftgröße **{{current}}** weicht von der erwarteten Schriftgröße \
**{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2004_invalid_hignote_size(linter, driver):
    """Ensure correct font size of highnote."""
    for footnote in driver.footnotes:
        if not footnote.style_number:
            continue
        current = footnote.style_number.size
        expected = driver.fontconfig.highnote_size
        if isinstance(expected, list):
            skip(f'ambiguous expected highnote size: {expected}')
            continue
        if utila.near(current, expected, HIGHNOTE_SIZE_DIFF_MAX):
            continue
        linter(
            number=footnote.number,
            current=current,
            expected=expected,
            location=iamraw.Location.from_page(footnote.page),
        )


SOLUTION_2005 = """\
Fußnote {{number}} falsch formatiert

Die Schriftart **{{current}}** weicht von der erwarteten Schriftart \
**{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2005_invalid_highnote_fontfamily(linter, driver):
    """Ensure correct font family of highnote."""
    for footnote in driver.footnotes:
        if not footnote.style_number:
            continue
        current = footnote.style_number.font
        expected = driver.fontconfig.highnote_fontid
        if isinstance(expected, list):
            skip(f'ambiguous expected highnote fontfamily: {expected}')
            continue
        current = driver.fontstore[current]
        expected = driver.fontstore[expected]
        if not current or not expected:
            skip('missing font, regenerate resources')
            continue
        current = current.name.lower()
        expected = expected.name.lower()
        if current == expected:
            continue
        linter(
            number=footnote.number,
            current=current,
            expected=expected,
            location=iamraw.Location.from_page(footnote.page),
        )


SOLUTION_2010 = """\
Fußnote {{number}} falsch formatiert

Die Schriftgröße **{{current}}** weicht von der erwarteten Schriftgröße \
**{{expected}}** ab.

{text/fussnote#formatierung}
"""


def check_2010_invalid_content_fontsize(linter, driver):
    """Ensure correct font size of footnote content."""
    for footnote in driver.footnotes:
        expected = driver.fontconfig.content_size
        if isinstance(expected, list):
            skip(f'ambiguous expected highnote fontsize:{expected}')
            continue
        if not footnote.style_text:
            protocol.skip_method('missing style')
            continue
        footnotestyle = footnote.style_text
        # The style of the last footnote includes the ending
        # whitespace/newline. This whitespace is formatted as next text token.
        # This is a result of requirements. The next token is the page number
        # with may differ in font size. Therefore we only validate text
        # positions which are characters.
        # do not check on whitespace or newline
        text = footnote.text
        footnotestyle = [
            item for item in footnotestyle if text[item.start:item.end].strip()
        ]
        # not not check highnotes inside footnote
        sizes = [
            item.size for item in footnotestyle if item.rise < RISE_NOISE_MAX
        ]
        sizes_equal = [
            utila.near(item, expected, CONTENT_SIZE_DIFF_MAX) for item in sizes
        ]
        if all(sizes_equal):
            continue
        linter(
            number=footnote.number,
            current=sizes,
            expected=expected,
            location=iamraw.Location.from_page(footnote.page),
        )
