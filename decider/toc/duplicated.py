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
import iamraw

import decider.toc


def validate(toc: iamraw.Toc) -> decider.toc.InvalidTocItems:
    flatten = decider.toc.flat(toc)

    lines = []
    for item in flatten:
        words = german.split_words(item.title, validate_sentences=False)
        words = decider.toc.remove_marks(words)
        lines.append(words)
    result = []
    duplication = duplicates(lines)
    for invalid in duplication:
        finding = [
            index for index, line in enumerate(flatten)
            if invalid[0] in line.title
        ]
        if not finding:
            continue
        result.append((invalid, finding))
    return result


DUPLICATES_MIN_COUNT = 5  # TODO: HOLY VALUE

# TODO: REPLACE WITH KONRAD APPROACH
NO_CONTENT = {'der', 'die', 'das', 'und', 'des', 'den'}


def duplicates(lines):
    counter = collections.Counter()
    for line in lines:
        for index in range(len(line)):
            for words in range(index + 1, len(line) + 1):
                tokens = line[index:words]
                if len(tokens) == 1 and tokens[0] in NO_CONTENT:
                    continue
                sub = ' '.join(tokens)
                counter[sub] += 1
    most_common = counter.most_common(n=100)
    result = [item for item in most_common if item[1] >= DUPLICATES_MIN_COUNT]
    return result
