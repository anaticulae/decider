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

import decider_footnote.path
import tests.footnote_


def test_highnote_inside_master89_page40(testdir, monkeypatch):  # pylint:disable=W0621
    """See 2010."""
    root = str(testdir)

    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {root} --style'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    style = decider_footnote.path.style(root)
    result = serializeraw.load_findings(style, 2010)

    result = [finding for finding in result if finding.location.page == 40]
    assert not result


def test_highnote_inside_master89_page45(testdir, monkeypatch):  # pylint:disable=W0621
    """Regression: Font size error on last footnote white space which is
    defined as following page number which differs in font size."""
    root = str(testdir)

    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {root} --style'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    style = decider_footnote.path.style(root)
    result = serializeraw.load_findings(style, 2010)

    result = [finding for finding in result if finding.location.page == 45]
    assert not result
