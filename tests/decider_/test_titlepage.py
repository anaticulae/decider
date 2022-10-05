# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest
import utila
import utilatest

import tests


def run_titlepage(src, expected, td, mp):
    if isinstance(expected, int):
        expected = [expected]
    # run decider
    cmd = f'-i {src} -o {td.tmpdir} --titlepage'
    tests.run(cmd, mp=mp)
    # validate result
    failures = [
        item.msgid for item in utila.flatten_content(
            protocol.findings_from_path(td.tmpdir))
    ]
    assert failures == expected, str(failures)


@pytest.mark.parametrize('src, expected', [
    pytest.param(power.MASTER116_PDF, 1210, id='master116'),
    pytest.param(
        power.MASTER072_PDF, 1221, id='master072', marks=pytest.mark.xfail),
    pytest.param(power.MASTER078_PDF, [], id='master078'),
])
def test_titlepage_extraction_default(src, expected, td, mp):
    utilatest.fixture_requires(src)
    src = power.link(src)
    run_titlepage(src, expected, td, mp)


@pytest.mark.parametrize('src, expected', [
    pytest.param(power.DOCU035_PDF, 1200, id='docu035'),
])
def test_titlepage_extraction_notitle(src, expected, td, mp):
    utilatest.fixture_requires(src, folder='notitle')
    src = power.link(src, folder='notitle')
    run_titlepage(src, expected, td, mp)
