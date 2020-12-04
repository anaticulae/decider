# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import german
import utila
import words.utils


def sentence_lookup(text) -> dict:
    lookup = collections.defaultdict(list)
    for page, sentence in words.utils.sentences(text):
        lookup[page].append(sentence)
    return dict(lookup)


def sentence_plain(sentence, marks) -> list:
    result = []
    splitted = german.split_words(sentence, validate_sentences=False)
    for start, end in marks:
        selected = [splitted[item] for item in utila.ranged_tuple(start, end)]
        selected = selection_plain(selected)
        result.append(selected)
    return result


def selection_plain(items: list) -> str:
    raw = ' '.join(items)
    raw = raw.replace('( ', '(')
    raw = raw.replace(' )', ')')
    return raw
