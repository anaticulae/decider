# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_footnote.features.footnote


def test_parsing_solution_definition():
    parsed = protocol.parse_solutions(decider_footnote.features.footnote)
    assert len(parsed) >= 1, parsed

    first = parsed[0]
    assert len(first.title) > 50, first.title
    assert '\n' not in first.title, first
    assert first.description


def test_parsing_validators_definition():
    parsed = protocol.parse_checkers(decider_footnote.features.footnote)
    assert len(parsed) >= 2, parsed
