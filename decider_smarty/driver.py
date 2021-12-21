# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw
import utila

import decider_smarty.utils


def create(
    badprefix: str = None,
    phrases: str = None,
    pleonasms: str = None,
    headlines: str = None,
    sentences: str = None,
    pages: tuple = None,
):
    # prepare findings
    if utila.exists(badprefix):
        badprefix = serializeraw.load_textadvices(badprefix, pages=pages)
    else:
        badprefix = None
    if utila.exists(phrases):
        phrases = serializeraw.load_textadvices(phrases, pages=pages)
    else:
        phrases = None
    if utila.exists(pleonasms):
        pleonasms = serializeraw.load_textadvices(pleonasms, pages=pages)
    else:
        pleonasms = None
    # content
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    sentences = serializeraw.load_text(
        sentences,
        headlines=headlines,
        pages=pages,
    )
    # sentences
    sentences = decider_smarty.utils.sentence_lookup(sentences)  # pylint:disable=R0204
    # driver
    driver = protocol.driver(
        badprefix=badprefix,
        phrases=phrases,
        pleonasms=pleonasms,
        sentences=sentences,
    )
    return driver
