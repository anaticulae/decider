# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def roman_to_arabic(number: str):
    # TODO: RELACE WITH LIBRARY
    common = {
        'I': 1,
        'II': 2,
        'III': 3,
        'IIII': 4,
        'IV': 4,
        'V': 5,
        'VI': 6,
        'VII': 7,
        'VIII': 8,
        'VIIII': 9,
        'IX': 9,
        'X': 10
    }
    return common[number]
