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

import decider_imgfig.path
import tests.imgfig_


def test_imgfig_min_quality(td, mp):
    source = power.link(power.BACHELOR076_PDF)
    tests.imgfig_.run(f'-i {source} --quality', mp=mp)

    loaded = serializeraw.load_findings(
        decider_imgfig.path.quality(td.tmpdir),
        msgids={4000},
    )
    # min dpi 96
    # dependent on min dpi definition
    assert len(loaded) in (12, 13)  # NOT VALIDATED


@pytest.mark.xfail(reason='broken rawmaker image extractor')
def test_imgfig_max_quality(td, mp):
    source = power.link(power.BACHELOR076_PDF)
    tests.imgfig_.run(f'-i {source} --quality', mp=mp)

    loaded = serializeraw.load_findings(
        decider_imgfig.path.quality(td.tmpdir),
        msgids={4001},
    )
    # max dpi = 2 * min dpi
    assert len(loaded) == 1  # dependent on max dpi definition


@pytest.mark.xfail(reason='broken rawmaker image extractor')
def test_imgfig_relation(td, mp):
    source = power.link(power.BACHELOR063_PDF)
    tests.imgfig_.run(f'-i {source} --quality', mp=mp)

    loaded = serializeraw.load_findings(
        decider_imgfig.path.quality(td.tmpdir),
        msgids={4005},
    )
    assert len(loaded) == 1
