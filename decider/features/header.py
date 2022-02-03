# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_header:

Header
======
"""

import collections
import typing

import configo
import protocol
import serializeraw

REPEATING_ITEM_RATIO_MAX = configo.HV_PERCENT_PLUS(default=30)


def work(headerfooter: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    loaded = serializeraw.load_headerfooter(headerfooter, pages=pages)
    headers = [item.header for item in loaded]

    linter.run(driver=headers)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_I2110 = """\
Kopfzeile: Redundanter Inhalt

Überprüfen Sie ob redundanter Inhalt:

<cite>
{{content}}
</cite>

wirklich nötig ist.
"""


def check_2110_repeating_header_content(linter, headers):
    if not headers:
        return
    collected = collections.defaultdict(set)
    for item in headers:
        if not item:
            # no header extracted
            continue
        for raw in item.undefined:
            collected[raw.text].add(item.page.value)
    for key, value in collected.items():
        percent = len(value) / len(headers) * 100
        if percent <= REPEATING_ITEM_RATIO_MAX:
            continue
        linter(content=key.strip())
