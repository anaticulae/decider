# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import decider.features.header


@pytest.mark.xfail(reason='software integration')
@utilatest.requires(power.TECH024_PDF)
def test_header_work():
    source = power.link(power.TECH024_PDF)
    headerfooter = iamraw.path.headerfooters(source)

    user, _ = decider.features.header.work(headerfooter)
    assert len(user) > 200, user

    loaded = serializeraw.load_findings(user)
    assert loaded[0].solution is not None, user[0]
