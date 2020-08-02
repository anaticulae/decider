# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol

import imgfig.path
import tests.imgfig_


def test_imgfig_cli_help(monkeypatch):
    tests.imgfig_.run('--help', monkeypatch=monkeypatch)


def test_imgfig_min_quality(testdir, monkeypatch):
    source = power.link(power.BACHELOR076_PDF)
    tests.imgfig_.run(f'-i {source} --quality', monkeypatch=monkeypatch)

    loaded = protocol.load_result(
        imgfig.path.quality(testdir.tmpdir),
        msgids={4000},
    )
    # min dpi 96
    assert len(loaded) == 5  # dependent on min dpi definition
