# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools
import string
import typing

import doctextstyle.parser
import doctextstyle.serialize
import protocol
import serializeraw
import texmex
import utila

MAX_HEADLINE_DIFF = 2.0  # TODO: HOLY VALUE

# TODO: USE VALIDATED TOC


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
        fontstore=fontstore,
        headlines=headlines,
        style=expected,
    )
    if not headlines:
        utila.error('no headlines given')
    if not navigators:
        utila.error('no navigators given')
    if navigators and headlines:
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


FONT_SIZE_ERROR = string.Template("""\
$title falsch formatiert

Die Schriftgröße **{%current%}** weicht von der
erwarteten Schriftgröße **{%expected%}** ab.
""")

FONT_FAMILY_ERROR = string.Template("""\
$title falsch formatiert

Die Schriftart **{%current%}** weicht von der
erwarteten Schriftart **{%expected%}** ab.
""")

FONT_DISTANCE_BEFORE_ERROR = string.Template("""\
$title falsch formatiert

Der Abstand vor der $title **{%current%}** weicht vom
erwarteten Abstand **{%expected%}** ab.
""")

FONT_DISTANCE_AFTER_ERROR = string.Template("""\
$title falsch formatiert

Der Abstand nach der $title **{%current%}** weicht vom
erwarteten Abstand **{%expected%}** ab.
""")

LEVEL_1 = 1  # TODO: HOLY VALUE

SOLUTION_7500 = FONT_SIZE_ERROR.substitute(title='Hauptüberschrift')


def check_7500_check_h1_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECLTY
    if not driver.style.h1_size:
        return

    validate_headline_size(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_size,
    )


SOLUTION_7501 = FONT_FAMILY_ERROR.substitute(title='Hauptüberschrift')


def check_7501_check_h1_font_family(linter: callable, driver):
    if not driver.style.h1_family:
        return

    validate_headline_family(
        linter,
        driver.navigators,
        driver.fontstore,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_family,
    )


SOLUTION_7502 = FONT_DISTANCE_BEFORE_ERROR.substitute(title='Hauptüberschrift')


def check_7502_check_h1_distance_before(linter: callable, driver):
    if not driver.style.h1_before:
        return

    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_before,
        check_before=True,
    )


SOLUTION_7503 = FONT_DISTANCE_AFTER_ERROR.substitute(title='Hauptüberschrift')


def check_7503_check_h1_distance_after(linter: callable, driver):
    if not driver.style.h1_after:
        return

    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_after,
        check_before=False,
    )


LEVEL_2 = 2  # TODO: HOLY VALUE

SOLUTION_7510 = FONT_SIZE_ERROR.substitute(title='Teilüberschrift')


def check_7510_check_h2_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECLTY
    if not driver.style.h2_size:
        return

    validate_headline_size(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_size,
    )


SOLUTION_7511 = FONT_FAMILY_ERROR.substitute(title='Teilüberschrift')


def check_7511_check_h2_font_family(linter: callable, driver):
    if not driver.style.h2_family:
        return

    validate_headline_family(
        linter,
        driver.navigators,
        driver.fontstore,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_family,
    )


SOLUTION_7512 = FONT_DISTANCE_BEFORE_ERROR.substitute(title='Teilüberschrift')


def check_7512_check_h2_distance_before(linter: callable, driver):
    if not driver.style.h2_before:
        return

    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_before,
        check_before=True,
    )


SOLUTION_7513 = FONT_DISTANCE_AFTER_ERROR.substitute(title='Teilüberschrift')


def check_7513_check_h2_distance_after(linter: callable, driver):
    if not driver.style.h2_after:
        return

    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_after,
        check_before=False,
    )


LEVEL_3 = 3  # TODO: HOLY VALUE

SOLUTION_7520 = FONT_SIZE_ERROR.substitute(title='Unterüberschrift')


def check_7520_check_h3_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECLTY
    if not driver.style.h3_size:
        return

    validate_headline_size(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_size,
    )


SOLUTION_7521 = FONT_FAMILY_ERROR.substitute(title='Unterüberschrift')


def check_7521_check_h3_font_family(linter: callable, driver):
    if not driver.style.h3_family:
        return

    validate_headline_family(
        linter,
        driver.navigators,
        driver.fontstore,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_family,
    )


SOLUTION_7522 = FONT_DISTANCE_BEFORE_ERROR.substitute(title='Unterüberschrift')


def check_7522_check_h3_distance_before(linter: callable, driver):
    if not driver.style.h3_before:
        return

    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_before,
        check_before=True,
    )


SOLUTION_7523 = FONT_DISTANCE_AFTER_ERROR.substitute(title='Unterüberschrift')


def check_7523_check_h3_distance_after(linter: callable, driver):
    if not driver.style.h3_after:
        return

    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_after,
        check_before=False,
    )


SOLUTION_7540 = """\
Kapitel beginnt nicht auf neuer Seite

Das Kapitel „{%chapter%}“ beginnt nicht auf einer neuen Seite. Fügen
Sie vor dem Kapitelstart einen Seitenumbruch ein.

{WORD}
Passen Sie dazu die **Formatvorlage der Überschriften** Level 1 an oder
verwenden Sie einen **manuellen Zeilenumbruch**.
{END}

* TODO: Article with explaination
{WORD}
* Formatvorlage anpassen
* Manueller Seitenumbruch
{END}
"""


def check_7540_chapter_on_new_page(linter: callable, driver):
    headlines = utila.flatten(driver.headlines)
    headlines = [headline for headline in headlines if headline.level == 1]
    for headline in headlines:
        start = container_start(headline.container)
        if start == 0:
            # chapter starts at page begin
            # TODO: CHECK FOR HEADER OR PAGE NUMBER BEFORE HEADLINE? MAY
            # BE NOT ZERO?
            continue
        containers_ = containers(headline.container)
        location = protocol.RangedLocation(
            page=headline.page,
            line=containers_[0],
            line_end=containers_[-1],
        )
        linter(
            location=location,
            chapter=headline.text,
        )


def validate_headline_size(
        linter,
        navigators,
        headlines,
        level,
        expected_size,
):
    flats = utila.flatten(headlines)
    headlines = [item for item in flats if item.level == level]
    for headline in headlines:
        containers_ = containers(headline.container)
        navigator = utila.select_page(navigators, headline.page)

        lines_selected = [navigator[index] for index in containers_]
        textsizes_ = container_textsizes(lines_selected)

        if all([item == expected_size for item in textsizes_]):
            continue

        # font size diff
        location = protocol.RangedLocation(
            page=headline.page,
            line=containers_[0],
            line_end=containers_[-1],
        )
        linter(
            location=location,
            expected=expected_size,
            current=', '.join([f'{item}' for item in textsizes_]),
        )


def validate_headline_family(
        linter,
        navigators,
        fontstore,
        headlines,
        level,
        expected_family,
):
    flats = utila.flatten(headlines)
    headlines = [item for item in flats if item.level == level]
    try:
        expected_family = fontstore[expected_family].name
    except KeyError:
        utila.error(f'no expected headline family: {expected_family}')
        return
    for headline in headlines:
        containers_ = containers(headline.container)
        navigator = utila.select_page(navigators, headline.page)

        lines_selected = [navigator[index] for index in containers_]
        textfamily_ = []
        for item in container_textfamily(lines_selected):
            try:
                textfamily_.append(fontstore[item].name)
            except KeyError:
                utila.error(f'headline - font not found: {item}')

        if all([item == expected_family for item in textfamily_]):
            continue

        # font family diff
        location = protocol.RangedLocation(
            page=headline.page,
            line=containers_[0],
            line_end=containers_[-1],
        )
        linter(
            location=location,
            expected=expected_family,
            current=', '.join([f'{item}' for item in textfamily_]),
        )


def validate_headline_distance(
        linter,
        navigators,
        headlines,
        level,
        expected_distance,
        check_before: bool = True,
):
    flats = utila.flatten(headlines)
    headlines = [item for item in flats if item.level == level]
    for headline in headlines:
        containers_ = containers(headline.container)
        navigator = utila.select_page(navigators, headline.page)
        distances = doctextstyle.parser.textdistances(navigator)

        if check_before:
            before = distances[containers_[0]][0]
            if before is None:
                continue
            if utila.near(before, expected_distance, diff=MAX_HEADLINE_DIFF):
                continue
        else:
            after = distances[containers_[-1]][1]
            if after is None:
                continue
            if utila.near(after, expected_distance, diff=MAX_HEADLINE_DIFF):
                continue

        # distance diff
        location = protocol.RangedLocation(
            page=headline.page,
            line=containers_[0],
            line_end=containers_[-1],
        )
        linter(
            location=location,
            expected=expected_distance,
            current=before if check_before else after,
        )


def container_start(item):
    with contextlib.suppress(TypeError):
        return item[0]
    return item


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


def container_textfamily(items):
    result = []
    for item in items:
        family = textfamily(item.style)
        result.extend(family)
    result = sorted(result)
    return result


def textsizes(style: texmex.TextInfo) -> utila.Floats:
    sizes = [item.size for item in style.content]
    sizes = utila.make_unique(sizes)
    result = sorted(sizes)
    return result


def textfamily(style: texmex.TextInfo) -> utila.Ints:
    fonts = [item.font for item in style.content]
    fonts = utila.make_unique(fonts)
    return fonts
