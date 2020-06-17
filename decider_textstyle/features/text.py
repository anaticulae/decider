# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import doctextstyle.parser
import doctextstyle.serialize
import iamraw
import iamraw.fonts
import protocol
import serializeraw
import serializeraw.border
import serializeraw.headerfooter
import utila

import decider_textstyle.utils


def work(  # pylint:disable=R0914
        textstyle: str,
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        fontheader: str,
        fontcontent: str,
        lists: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    expected = doctextstyle.serialize.load_docstyle(textstyle)
    headlines = serializeraw.load_headlines(headlines, pages=pages)

    lists = serializeraw.load_lists(lists, pages=pages) if lists else []

    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborders,
        headerfooterpath=headerfooter,
        fontheader=fontheader,
        fontcontent=fontcontent,
        pages=pages,
    )

    if not headlines:
        utila.error('no headlines given')
    if not navigators:
        utila.error('no navigators given')

    if navigators and headlines:
        # TODO: DO WE REALY REQUIRE HEADLINES?
        chunks = decider_textstyle.utils.text_chunks(
            headlines,
            navigators,
            lists,
            sync=True,  # TODO: REMOVE?
            yieldnone=True,
        )
        data = protocol.driver(
            text_chunks=chunks,
            fontstore=fontstore,
            headlines=headlines,
            style=expected,
        )
        linting(data, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(driver, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
        )
        checker(call, driver)


SOLUTION_7550 = """\
Schriftgröße des Texts weicht ab

Die erkannte Schriftgröße **{%current%}** weicht von
der erwarteten Schriftgröße **{%expected%}**.
"""


def check_7550_check_text_size(linter: callable, driver):
    if not driver.style.text_size:
        return
    chunks = driver.text_chunks
    expected = driver.style.text_size
    for page, line, item in chunks:
        if not item:
            continue
        textsize = item.style.textsize()
        if textsize == expected:
            continue

        location = protocol.RangedLocation(page=page, line=line)
        # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
        linter(location=location, expected=expected, current=textsize)


SOLUTION_7551 = """\
Schriftart des Texts weicht ab

Die erkannte Schriftart **{%current%}** weicht von
der erwarteten Schriftart **{%expected%}** ab.
"""


def check_7551_check_text_family(linter: callable, driver):
    if not driver.style.text_family:
        return
    chunks = driver.text_chunks
    expected = driver.fontstore[driver.style.text_family].name
    for page, line, item in chunks:
        if not item:
            continue
        for style in item.style:
            if style.font == iamraw.NO_FONT:
                utila.error(f'no font for {page} {line} {item}')
                continue
            current = driver.fontstore[style.font].name
            if current == expected:
                continue
            location = protocol.RangedLocation(
                page=page,
                line=line,
                token=style.start,
                token_end=style.end,
            )
            # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
            linter(location=location, expected=expected, current=current)


SOLUTION_7555 = """\
Text: Unzulässige Markierung

Der Text weist unnötige Hervorhebungen auf. Es ist nicht nötig den Leser
durch typografische Veränderungen auf besonders `wichtige` Punkte
hinzuweisen. Dies erschwert den Lesefluss.

TODO: SIEHE ARTIKEL THEISSEN
"""


def check_7555_text_bold(linter: callable, driver):
    chunks = driver.text_chunks
    for page, line, item in chunks:
        if not item:
            continue
        for style in item.style:
            if style.font == iamraw.NO_FONT:
                utila.error(f'no font for {page} {line} {item}')
                continue
            current = driver.fontstore[style.font]
            if current.weight != iamraw.fonts.Weight.BOLD:
                # TODO: EXCLUDE TABLE HEADLINES ETC.
                continue
            location = protocol.RangedLocation(
                page=page,
                line=line,
                token=style.start,
                token_end=style.end,
            )
            # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
            linter(location=location)
