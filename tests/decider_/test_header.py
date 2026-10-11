# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw.path
import serializeraw
import utilotest

import decider.features.header


@utilotest.requires(hoverpower.TECH024_PDF)
def test_header_work():
    source = hoverpower.link(hoverpower.TECH024_PDF)
    headerfooter = iamraw.path.headerfooters(source)

    user, _ = decider.features.header.work(headerfooter)
    assert len(user) > 200, user

    loaded = serializeraw.load_findings(user)
    assert loaded[0].solution is not None, user[0]
