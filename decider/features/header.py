# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_header:

Header
======
"""
import collections
import functools
import typing

import configo
import protocol
import serializeraw

MAX_REPEATING_ITEM_RATIO = configo.HV_PERCENT_PLUS(default=30).value


def work(headerfooter: str, pages: tuple = None) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

    loaded = serializeraw.load_headerfooter(headerfooter, pages=pages)
    headers = [item.header for item in loaded]

    linting(headers, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(
        headers,
        linter: protocol.Linter,
):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
        )
        checker(call, headers)


SOLUTION_2110 = """\
Kopfzeile: wiederholdender Inhalt

Überprüfen Sie ob redundanter Inhalt:

<cite>
{%content%}
</cite>

wirklich nötig ist.
"""


def check_2110_repeating_header_content(linter, headers):
    if not headers:
        return
    collected = collections.defaultdict(set)
    for item in headers:
        for raw in item.undefined:
            collected[raw.text].add(item.page.value)
    for key, value in collected.items():
        percent = len(value) / len(headers) * 100
        if percent <= MAX_REPEATING_ITEM_RATIO:
            continue
        linter(content=key.strip())
