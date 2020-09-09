# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import protocol
import serializeraw
import utila

import decider_textstyle.utils


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


def textdata(
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        lists=None,
        magiccontent=None,
        textstyle=None,
        pages=None,
):
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
    # TODO: DO WE REQUIRE HEADLINES?
    # if not headlines or not navigators:
    #     return None
    if not navigators:
        return None
    chunks = decider_textstyle.utils.text_chunks(
        headlines,
        navigators,
        magiccontent=magiccontent,
    )
    if not magiccontent:
        nomagic = chunks
    else:
        nomagic = decider_textstyle.utils.text_chunks(
            headlines,
            navigators,
        )
    if textstyle:
        return protocol.driver(
            text_chunks=chunks,
            nomagic_text_chunks=nomagic,
            doctextstyle=textstyle,
        )
    return protocol.driver(text_chunks=chunks, nomagic_text_chunks=nomagic)
