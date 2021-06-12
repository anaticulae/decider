# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import iamraw
import protocol
import serializeraw
import textflow.quotation.serialize
import utila

import decider_textflow.utils


def linting(name, driver=None):
    # IMPORTANT TODO: WITHOUT DRIVER, NOTHING HAPPEN HERE?
    linter = protocol.from_module(name)
    if driver:
        # run linting if data is provided
        checkers = protocol.parse_checkers(name)
        for checker in checkers:
            call = functools.partial(
                linter.add_finding,
                msgid=checker.msgid,
            )
            checker(call, driver)
    # write result
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def textdata(  # pylint:disable=R0913
    headlines,
    text,
    textpositions,
    sizeandborders,
    headerfooter,
    lists=None,
    magiccontent=None,
    textstyle=None,
    magicvalid=None,
    quotations=None,
    pages=None,
):
    if magicvalid is None:
        magicvalid = iamraw.TEXTUAL  # pylint:disable=E1101
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborders,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    lists = serializeraw.load_lists(lists, pages=pages) if lists else []
    if not headlines:
        utila.error('no headlines given')
    if not navigators:
        utila.error('no navigators given')
    if utila.exists(magiccontent):
        magiccontent = serializeraw.load_magic_types(magiccontent, pages=pages)
    else:
        magiccontent = None
    # TODO: DO WE REQUIRE HEADLINES?
    # if not headlines or not navigators:
    #     return None
    if not navigators:
        return None
    chunks = decider_textflow.utils.text_chunks(
        headlines,
        navigators,
    )
    nomagic = decider_textflow.utils.text_chunks(
        headlines,
        navigators,
        magiccontent=magiccontent,
        magicvalid=magicvalid,
    )
    if utila.exists(quotations):
        quotations = textflow.quotation.serialize.load_quotations(
            quotations,
            pages=pages,
        )
    else:
        quotations = None
    if textstyle:
        return protocol.driver(
            text_chunks=chunks,
            nomagic_text_chunks=nomagic,
            doctextstyle=textstyle,
            quotations=quotations,
        )
    return protocol.driver(
        text_chunks=chunks,
        nomagic_text_chunks=nomagic,
        quotations=quotations,
    )
