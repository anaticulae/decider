# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_header:

Header
======
"""

import collections

import configos
import protoerror
import serializeraw

REPEATING_ITEM_RATIO_MAX = configos.HV_PERCENT_PLUS(default=30)


def work(headerfooter: str, pages: tuple = None) -> tuple[str, str]:
    linter = protoerror.from_module(__name__)

    loaded = serializeraw.load_headerfooter(headerfooter, pages=pages)
    headers = [item.header for item in loaded]

    linter.run(driver=headers)

    result = linter.result(unique=True)
    user, developer = protoerror.dump_result(result)
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
        # TODO: ENSURE THAT ITEM.PAGE IS NOT NONE
        pagenumber = item.page.value if item.page is not None else -1
        for raw in item.undefined:
            collected[raw.text].add(pagenumber)
    for key, value in collected.items():
        percent = len(value) / len(headers) * 100
        if percent <= REPEATING_ITEM_RATIO_MAX:
            continue
        linter(
            content=key.strip(),
            location=protoerror.OVERVIEW,
        )
