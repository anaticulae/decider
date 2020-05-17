# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import contextlib
import functools
import typing

import doctextstyle.serialize
import protocol
import serializeraw
import texmex
import utila


def work(
        textstyle: str,
        headlines: str,
        text: str,
        textpositions: str,
        fontheader: str,
        fontcontent: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    expected = doctextstyle.serialize.load_docstyle(textstyle)
    headlines = serializeraw.load_headlines(headlines, pages=pages)

    # TODO: CREATE SEPARATE METHOD
    text = serializeraw.load_document(text, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)
    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    navigators = texmex.create_pagetextnavigators(
        text,
        textpositions,
        fontstore,
    )

    data = protocol.driver(
        navigators=navigators,
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


SOLUTION_7500 = """\
Hauptüberschrift falsch formatiert

Die Schriftgröße {%current%} weicht von der
erwarteten Schriftgröße {%expected%} ab.
"""

LEVEL_1 = 1  # TODO: HOLY VALUE


def check_7500_check_h1_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECLTY
    headlines = driver.headlines
    navigators = driver.navigators
    if not headlines:
        # TODO: ADD LINTING TO SIGNAL TO DEVELOPER THAT THERE ARE NO HEADLINES?
        return
    if not navigators:
        return
    h1_fontsize_expected = driver.style.h1_size
    if not h1_fontsize_expected:
        return
    flats = utila.flatten(headlines)
    h1_headlines = [item for item in flats if item.level == LEVEL_1]
    for headline in h1_headlines:
        containers_ = containers(headline.container)
        navigator = utila.select_page(navigators, headline.page)

        lines_selected = [navigator[index] for index in containers_]
        textsizes_ = container_textsizes(lines_selected)

        if all([item == h1_fontsize_expected for item in textsizes_]):
            continue

        # font size diff
        location = protocol.RangedLocation(
            page=headline.page,
            line=containers_[0],
            line_end=containers_[-1],
        )
        linter(
            location=location,
            expected=h1_fontsize_expected,
            current=textsizes_,
        )


def containers(item) -> tuple:
    with contextlib.suppress(TypeError):
        return tuple(range(item[0], item[1] + 1))
    return (item,)


def container_textsizes(items):
    result = []
    for item in items:
        sizes = textsizes(item.style)
        result.extend(sizes)
    result = sorted(result)
    return result


def textsizes(style: texmex.TextInfo) -> float:
    sizes = [item.size for item in style.content]
    sizes = utila.make_unique(sizes)
    result = sorted(sizes)
    return result
