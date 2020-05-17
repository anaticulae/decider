# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.feature.distance
import groupme.path
import protocol
import pytest

import border.features.distance
import tests.resources


@pytest.mark.parametrize('page, expected', [
    (0, 0),
    (5, 6),
])
def test_border_distances_linting(page, expected):
    area = groupme.path.area(tests.resources.PYPORTING)
    distance = groupme.path.distance(tests.resources.PYPORTING)

    dumped_findings = border.features.distance.work(area, distance, pages=page)
    findings = protocol.load_result(dumped_findings[0])
    assert len(findings) == expected, findings
