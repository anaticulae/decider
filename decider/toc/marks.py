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

import decider.toc


def validate_question_mark(toc: iamraw.Toc) -> decider.toc.InvalidTocItems:
    flatten = decider.toc.flat(toc)

    lines = []
    for index, item in enumerate(flatten):
        words = german.split_words(item.title, validate_sentences=False)

        contains_question = any(
            [item == konrad.Mark.QUESTION_MARK for item in words])

        if contains_question:
            lines.append((index, item.title, item.raw_location))
    return lines


def collect_quotation_marks(toc: iamraw.Toc) -> decider.toc.InvalidTocItems:
    flatten = decider.toc.flat(toc)

    lines = []
    for index, item in enumerate(flatten):
        words = german.split_words(item.title, validate_sentences=False)
        if not german.contain_quotation_marks(words):
            continue
        lines.append((index, item.title, item.raw_location))
    return lines
