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
import power
import protocol
import pytest

import border.features.distance


@pytest.mark.parametrize('page, expected', [
    (0, 0),
    (5, 6),
])
def test_border_distances_linting(page, expected):
    area = groupme.path.area(power.link(power.DOCU07_PDF))
    distance = groupme.path.distance(power.link(power.DOCU07_PDF))

    dumped_findings = border.features.distance.work(area, distance, pages=page)
    findings = protocol.load_result(dumped_findings[0])
    assert len(findings) == expected, findings
