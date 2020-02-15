# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider.utils


def test_decider_bounding_location_from_str():
    example = 'b(123.5;100.0;500.0;500.0)p5'
    parsed = decider.utils.BoundingLocation.fromstr(example)

    assert parsed.value == (123.5, 100.0, 500.0, 500.0), parsed.value


def test_decider_bounding_location_dump_load():
    example = decider.utils.BoundingLocation.fromtuple(
        (5.0, 10.0, 50.0, 50.0),
        page=36,
    )
    dumped = str(example)
    loaded = decider.utils.BoundingLocation.fromstr(dumped)
    assert loaded == example
