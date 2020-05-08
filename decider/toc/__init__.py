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

import collections

import iamraw
import iamraw.toc


class InvalidTocItems(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result


def remove_marks(items: list) -> list:
    # TODO: REPLACE WITH KONRAD CODE
    assert isinstance(items, list), type(items)
    result = [item for item in items if isinstance(item, str)]
    return result
