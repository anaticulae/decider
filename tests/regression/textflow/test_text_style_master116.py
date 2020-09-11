# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import decider_textflow
import tests.textflow_


@pytest.mark.xfail(reason='update hey data test generator')
def test_paragraph_too_short_in_table_master116_page79(testdir, monkeypatch):
    source = power.link(power.MASTER116_PDF)
    cmd = f'-i {source}  --paragraph --pages=79'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textflow.path.paragraph_linted(testdir.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7630})
    assert loaded[0].location.line == 10 and loaded[0].location.line_end == 11
    assert loaded[1].location.line == 13 and loaded[1].location.line_end == 15
    assert loaded[2].location.line == 26 and loaded[2].location.line_end == 28
