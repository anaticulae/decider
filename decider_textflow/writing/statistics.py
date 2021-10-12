# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import dataclasses
import statistics

import german
import iamraw
import utila


@dataclasses.dataclass
class WritingStatistics:
    words: int = None
    sentences: int = None

    word_avg: float = None
    sentence_avg: float = None

    word_min: int = None
    word_max: int = None

    sentence_min: int = None
    sentence_max: int = None


SENTENCE_LENGTH_MIN = 7


def determine(sentences) -> WritingStatistics:
    result = WritingStatistics()
    sento = []
    words = collections.defaultdict(int)
    for sentence in determine_sentences(sentences):
        for word in sentence:
            words[word] += 1
        sento.append(len(sentence))
    if not words:
        # no data given, skip analysis
        return None
    result.words = sum(words.values())
    result.sentences = len(sento)

    result.word_min = sorted(words.keys(), key=len)[0]
    result.word_max = sorted(words.keys(), key=len)[-1]
    result.sentence_min = min(sento)
    result.sentence_max = max(sento)

    wordo = utila.flatten([[len(key)] * value for key, value in words.items()])
    result.word_avg = statistics.mean(wordo)
    result.sentence_avg = statistics.mean(sento)

    result.word_avg: float = utila.roundme(result.word_avg)
    result.sentence_avg: float = utila.roundme(result.sentence_avg)
    return result


def determine_sentences(sentences):
    for sentence in sentences:
        if isinstance(sentence, iamraw.Headline):
            continue
        txt = sentence[0]
        if len(txt) < SENTENCE_LENGTH_MIN:
            continue
        sento = word_tokenize(txt)
        if not sento:
            continue
        if len(sento) < 3:
            continue
        yield sento


def word_tokenize(txt: str) -> list:
    tokens = german.word_tokenize(txt, validate_sentences=False)
    tokens = [item.lower() for item in tokens if isinstance(item, str)]
    tokens = [item for item in tokens if utila.char_rate(item) == 1.0]
    tokens = [item for item in tokens if len(item) >= 2]
    return tokens
