# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import imgfig.features.position
import imgfig.path
import tests.imgfig_


def test_imgfig_position_alignment(testdir, monkeypatch):
    source = power.link(power.MASTER091B_PDF)
    tests.imgfig_.run(
        f'-i {source} --position --pages=0:50',
        monkeypatch=monkeypatch,
    )
    loaded = serializeraw.load_findings(
        imgfig.path.position(testdir.tmpdir),
        msgids={4031},
    )
    assert len(loaded) == 8


def test_imgfig_position_unclear(testdir, monkeypatch):
    source = power.link(power.MASTER091B_PDF)
    with monkeypatch.context() as context:
        # use high required trust to invoke error
        context.setattr(
            imgfig.features.position,
            'ALIGNMENT_TRUST_MIN',
            0.9,
        )
        tests.imgfig_.run(
            f'-i {source} --position --pages=0:50',
            monkeypatch=monkeypatch,
        )
    loaded = serializeraw.load_findings(
        imgfig.path.position(testdir.tmpdir),
        msgids={4030},
    )
    assert len(loaded) == 1
