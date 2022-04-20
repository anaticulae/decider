# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import protocol
import serializeraw
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


def create_driver(  # pylint:disable=R0913,R0914
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
    words=None,
    pages=None,
):
    assert magiccontent is None or isinstance(magiccontent, str), 'require path'
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
    if not navigators:
        utila.error('no navigators given')
        return None
    lists = serializeraw.load_lists(lists, pages=pages) if lists else []
    if not headlines:
        utila.error('no headlines given')
    if utila.exists(magiccontent):
        magiccontent = serializeraw.load_magic_types(magiccontent, pages=pages)
    else:
        magiccontent = None
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
        quotations = serializeraw.load_quotations(
            quotations,
            pages=pages,
        )
    else:
        # empty quotations
        # Hint: Empty list is required to avoid failing later algorithms.
        quotations = []
    sentences = []
    if words:
        words = serializeraw.load_text(
            words,
            headlines,
            pages=pages,
        )
        sentences: Sentences = Sentences(words)
    headlines_confidence = 1.0
    if headlines:
        try:
            # TODO: REMOVE LATER AFTER UPGRADING IAMRAW
            headlines_confidence = headlines.confidence
        except AttributeError:
            utila.error('require headlines.confidence, use 1.0')
    if textstyle:
        return protocol.driver(
            text_chunks=chunks,
            nomagic_text_chunks=nomagic,
            doctextstyle=textstyle,
            quotations=quotations,
            sentences=sentences,
            headlines_confidence=headlines_confidence,
        )
    return protocol.driver(
        text_chunks=chunks,
        nomagic_text_chunks=nomagic,
        quotations=quotations,
        sentences=sentences,
        headlines_confidence=headlines_confidence,
    )


class Sentences:

    def __init__(self, words):
        self.content = []
        for contenttext in words:
            for textsection in contenttext.content:
                # yield headline
                if textsection.headline and textsection.headline.container != -1:
                    # TODO: IS HEADLINE IMPORTANT? THIS MAY PRODUCE AN ERROR LATER?
                    self.content.append(textsection.headline)
                merged = list(
                    zip(
                        textsection.content,
                        textsection.pages,
                        range(len(textsection.pages)),
                    ))
                self.content.extend(merged)

    def __getitem__(self, index):
        return self.content[index]
