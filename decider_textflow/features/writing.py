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

import german
import iamraw
import protocol
import serializeraw
import utila

import decider_textstyle.utils


def work(  # pylint:disable=R0914
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    navigators = decider_textstyle.utils.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborders,
        headerfooterpath=headerfooter,
        pages=pages,
    )

    if not headlines:
        utila.error('no headlines given')
    if not navigators:
        utila.error('no navigators given')

    linter = protocol.from_module(__name__)
    if navigators and headlines:
        chunks = decider_textstyle.utils.text_chunks(
            headlines,
            navigators,
        )
        data = protocol.driver(text_chunks=chunks)
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


SOLUTION_7600 = """\
Fehler in der Persepektive

**{%invalid%}** sollte vermieden werden.

TODO: ADD ARTICLE
"""

# TODO: REPLACE WITH EXTERNAL METHOD
INVALID_PERSPECTIVE = {'wir', 'man', 'Wir', 'Man'}


def check_7600_text_perspective(linter: callable, driver):
    text = driver.text_chunks
    for page, line, item in text:
        if isinstance(item, iamraw.Headline):
            continue

        words = german.split_words(item.text, validate_sentences=False)
        words = [item.lower() for item in words if isinstance(item, str)]
        # TODO: DO NOT LINT IN QUOTATION
        invalid = [item for item in words if item in INVALID_PERSPECTIVE]
        if not invalid:
            continue
        location = protocol.RangedLocation(page=page, line=line)
        linter(location=location, invalid=', '.join(invalid))
