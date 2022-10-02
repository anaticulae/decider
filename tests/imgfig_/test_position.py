# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import decider_imgfig.features.position
import decider_imgfig.path
import tests.imgfig_


@utilatest.requires(power.MASTER091B_PDF)
def test_imgfig_position_alignment(td, mp):
    source = power.link(power.MASTER091B_PDF)
    tests.imgfig_.run(
        f'-i {source} --position --pages=0:50',
        mp=mp,
    )
    loaded = serializeraw.load_findings(
        decider_imgfig.path.position(td.tmpdir),
        msgids={4031},
    )
    # -1: skip title page adjustment error
    assert len(loaded) == 6 - 1  # TODO: VALIDATE LATER


@utilatest.requires(power.MASTER091B_PDF)
def test_imgfig_position_unclear(td, mp):
    source = power.link(power.MASTER091B_PDF)
    with mp.context() as context:
        # use high required trust to invoke error
        context.setattr(
            decider_imgfig.features.position,
            'ALIGNMENT_TRUST_MIN',
            0.9,
        )
        tests.imgfig_.run(
            f'-i {source} --position --pages=0:50',
            mp=mp,
        )
    loaded = serializeraw.load_findings(
        decider_imgfig.path.position(td.tmpdir),
        msgids={4030},
    )
    assert len(loaded) == 1


@pytest.mark.xfail(reason='improve image/figure detector')
@utilatest.requires(power.MASTER031_PDF)
def test_imgfig_skip_title_legal_etc(td, mp):
    """Do not judge image position on title page or legal information."""
    source = power.link(power.MASTER031_PDF)
    tests.imgfig_.run(
        f'-i {source} --position',
        mp=mp,
    )
    loaded = serializeraw.load_findings(
        decider_imgfig.path.position(td.tmpdir),
        msgids={4031},
    )
    # TODO: ADD SUPPORT FOR TEXT INLINED IMAGES
    assert len(loaded) == 1  # TODO: VALIDATE LATER
