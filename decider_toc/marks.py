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

import decider_toc.utils as dtu


def validate_question_mark(toc: iamraw.Toc) -> dtu.InvalidTocItems:
    result = collect_mark(toc, konrad.Mark.QUESTION_MARK)
    return result


def validate_general_marks(toc: iamraw.Toc) -> dtu.InvalidTocItems:
    result = collect_mark(toc, (
        konrad.Mark.EXCLAMATION_MARK,
        konrad.Mark.COMMA,
    ))
    return result


def collect_mark(toc: iamraw.Toc, mark: konrad.Mark) -> dtu.InvalidTocItems:
    flatten = dtu.flat(toc)
    marks = [mark] if isinstance(mark, konrad.Mark) else mark

    result = []
    for index, item in enumerate(flatten):
        words = german.split_words(item.title, validate_sentences=False)
        contains_mark = any([item in marks for item in words])
        if contains_mark:
            result.append((index, item.title, item.raw_location))
    return result


def collect_quotation_marks(toc: iamraw.Toc) -> dtu.InvalidTocItems:
    flatten = dtu.flat(toc)
    lines = []
    for index, item in enumerate(flatten):
        words = german.split_words(item.title, validate_sentences=False)
        if not german.contain_quotation_marks(words):
            continue
        lines.append((index, item.title, item.raw_location))
    return lines
