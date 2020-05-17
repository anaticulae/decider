# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import iamraw.path
import protocol

import decider.features.header
import tests.resources


def test_header_work():
    headerfooter = iamraw.path.headerfooters(
        tests.resources.TECHNICAL24)

    user, _ = decider.features.header.work(headerfooter)
    assert len(user) > 200, user

    loaded = protocol.load_result(user)
    assert loaded[0].solution is not None, user[0]
