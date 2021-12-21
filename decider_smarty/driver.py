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

import decider_smarty.utils


def create(
    invalid_prefix: str,
    phrases: str,
    pleonasms: str,
    headlines: str,
    sentences: str,
    pages: tuple = None,
):
    # prepare findings
    invalid_prefix = serializeraw.load_textadvices(invalid_prefix, pages=pages)
    phrases = serializeraw.load_textadvices(phrases, pages=pages)
    pleonasms = serializeraw.load_textadvices(pleonasms, pages=pages)
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
        invalid_prefix=invalid_prefix,
        phrases=phrases,
        pleonasms=pleonasms,
        sentences=sentences,
    )
    return driver
