# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import decider_textflow.path
import tests
import tests.textflow_


def test_startend_hurenkind_bachelor90_page16(testdir, monkeypatch):
    """After oneline a headline follow which marks a `Hurenkind`. Load
    one page before and one page after to load required headlines."""
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i={source} --startend --pages=15:17'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = serializeraw.load_findings(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7620,
    )
    assert len(result) == 1, str(result)


def test_startend_hurenkind_bachelor90_page18(testdir, monkeypatch):
    """After a short line a full line follow, which marks a `Hurenkind`.
    Load one page before and one page after to load required
    headlines."""
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i={source} --startend --pages=17:19'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = serializeraw.load_findings(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7620,
    )
    assert len(result) == 1, str(result)


def test_startend_figure_start_bachelor90_page40_55(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i={source} --startend --pages=40:55'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = serializeraw.load_findings(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7625,
    )
    assert len(result) == 3, str(result)


def test_startend_figure_start_bachelor90_page34(testdir, monkeypatch):
    """Ensure to detect page starts with an image instead of text."""
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i={source} --startend --pages=34:40'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = serializeraw.load_findings(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7625,
    )
    assert len(result) == 1, str(result)
