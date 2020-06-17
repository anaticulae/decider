# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import konrad

import decider_toc.utils

MAX_WORD_COUNT = 12  # TODO: HOLY VALUE


def validate(toc: iamraw.Toc) -> decider_toc.utils.InvalidTocItems:
    flatten = decider_toc.utils.flat(toc)

    lines = []
    for index, item in enumerate(flatten):
        words = german.split_words(item.title, validate_sentences=False)
        words = konrad.remove_marks(words)
        linelength = len(words)
        if linelength > MAX_WORD_COUNT:
            lines.append((index, item.title, linelength, item.raw_location))
    return lines
