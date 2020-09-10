# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of Content
================

Principle
---------

.. note:: see Mario Rene Theisen: Wissenschaftliches Arbeiten, page 118-120

Linienprinzip
~~~~~~~~~~~~~

    .. code-block:: none

        1 Gebrauchsanweisung
        2 Der wissenschaftliche Arbeitsprozess
            2.1 Planung
                2.1.1 Projektplanung
                2.1.2 Kostenplanung
            2.2 Vorarbeiten

* pro:

    1.

    2.

* contra:

    1. do not differentiate to deep, max 3-4 level

    2.


Abstufungsprinzip
~~~~~~~~~~~~~~~~~

    .. code-block:: none

        A Lateinische Buchstaben
            I. Roman numbers
                1. Arabische Zahlen
                    a. Lateinische Kleinbuchstaben
        B ...

* pro:
    1. easy to differentiate and orientate

    2.

* contra:
    1.
    2.
"""

import contextlib

import utila

import decider
import decider_toc.__iamraw__

ROOT = decider.ROOT

__version__ = decider.__version__

PROCESS = 'decider_toc'


def isroman(item) -> bool:
    # TODO: REMOVE AFTER UPGRADE
    """\
    >>> isroman('XII')
    True
    >>> isroman('10')
    False
    >>> isroman(10)
    False
    """
    with contextlib.suppress(KeyError):
        _ = arabic(item)
        return True
    return False


def arabic(*items) -> int:
    """Converst Roman to Arabic numbers.

    >>> arabic('XII')
    12
    >>> arabic('I', 'IIII', 'VI', 'VIIII')
    [1, 4, 6, 9]
    """
    result = []
    for item in items:
        item = str(item).upper()
        try:
            result.append(NUMBERS[item])
        except KeyError:
            result.append(EXCEPTION[item])
    if len(result) == 1:
        return result[0]
    return result


NUMBERS = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12,
    'XIII': 13,
    'XIV': 14,
    'XV': 15,
    'XVI': 16,
    'XVII': 17,
    'XVIII': 18,
    'XIX': 19,
    'XX': 20,
    'XXI': 21,
    'XXII': 22,
    'XXIII': 23,
    'XXIV': 24,
    'XXV': 25,
    'XXVI': 26,
    'XXVII': 27,
    'XXVIII': 28,
    'XXIX': 29,
    'XXX': 30,
    'XXXI': 31,
    'XXXII': 32,
    'XXXIII': 33,
    'XXXIV': 34,
    'XXXV': 35,
    'XXXVI': 36,
    'XXXVII': 37,
    'XXXVIII': 38,
    'XXXIX': 39,
    'XL': 40
}

EXCEPTION = {
    'VIIII': 9,
    'IIII': 4,
    'XIIII': 14,
    'XXVIIII': 29,
    'XXXIIII': 34,
    'XXXVIIII': 39
}

utila.isroman = isroman
