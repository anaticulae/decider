# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol

import decider_textflow.path
import tests
import tests.resources
import tests.textflow_


def test_startend_hurenkind_bachelor90_page16(testdir, monkeypatch):  # pylint:disable=W0621
    """After oneline a headline follow which marks a `Hurenkind`. Load
    one page before and one page after to load required headlines."""
    source = tests.resources.BACHELOR90
    cmd = f'-i={source} --startend --pages=15:17'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = protocol.load_result(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7620,
    )
    assert len(result) == 1, str(result)


def test_startend_hurenkind_bachelor90_page18(testdir, monkeypatch):  # pylint:disable=W0621
    """After a short line a full line follow, which marks a `Hurenkind`.
    Load one page before and one page after to load required
    headlines."""
    source = tests.resources.BACHELOR90
    cmd = f'-i={source} --startend --pages=17:19'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = protocol.load_result(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7620,
    )
    assert len(result) == 1, str(result)


def test_startend_figure_start_bachelor90_page40_55(testdir, monkeypatch):  # pylint:disable=W0621
    source = tests.resources.BACHELOR90
    cmd = f'-i={source} --startend --pages=40:55'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = protocol.load_result(
        decider_textflow.path.startend_linted(testdir.tmpdir),
        7625,
    )
    assert len(result) == 3, str(result)
