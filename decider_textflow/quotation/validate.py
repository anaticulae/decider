# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: MOVE TO DUDEN PACKAGE?

import words.text.word

DOUBLE_OPEN = words.text.word.Mark.QUOTATION_MARK_DOUBLE_OPEN
DOUBLE_CLOSE = words.text.word.Mark.QUOTATION_MARK_DOUBLE_CLOSE
SINGLE_OPEN = words.text.word.Mark.QUOTATION_MARK_SINGLE_OPEN
SINGLE_CLOSE = words.text.word.Mark.QUOTATION_MARK_SINGLE_CLOSE


def german_double_quotation_closed(token: list) -> bool:
    open_close = [item for item in token if item in (DOUBLE_OPEN, DOUBLE_CLOSE)]
    if not open_close:
        return True
    double_open = [item for item in open_close if item == DOUBLE_OPEN]
    double_close = [item for item in open_close if item == DOUBLE_CLOSE]
    return len(double_open) == len(double_close)


DOUBLE_INSIDE_DOUBLE = words.text.word.split_words(
    '„zu diesem „etwas“ kontrollieren kann“.')

NO_DOUBLE_INSIDE_DOUBLE = words.text.word.split_words(
    "„zu diesem 'etwas' kontrollieren kann“.")


def german_no_double_quotes_inside_double(token: list) -> bool:
    """Check if single quotation are used in citation.

    >>> german_no_double_quotes_inside_double(DOUBLE_INSIDE_DOUBLE)
    False
    >>> german_no_double_quotes_inside_double(NO_DOUBLE_INSIDE_DOUBLE)
    True
    """
    open_close = [item for item in token if item in (DOUBLE_OPEN, DOUBLE_CLOSE)]
    # ensure alernating
    if not open_close:
        return True
    for current, after in zip(open_close[0:-1], open_close[1:]):
        if current == after:
            # require single marks inside
            # wrong: „zu diesem „etwas“ kontrollieren kann“.
            return False
    return True


def valid_double_marks_count_english(token: list):
    # TODO: DOUBLE_OPEN IS CURRENTLY GERMAN OPEN
    german_open = [item for item in token if item == DOUBLE_OPEN]
    if any(german_open):
        return False
    return True


def valid_single_marks_count(token: list) -> bool:
    assert isinstance(token, list), type(token)
    single_open = [item for item in token if item == SINGLE_OPEN]
    single_close = [item for item in token if item == SINGLE_CLOSE]

    valid = len(single_open) == len(single_close)
    return valid
