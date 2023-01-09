# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_footnote.path
import tests.footnote_


@utilatest.requires(power.MASTER089_PDF)
def test_highnote_inside_master89_page40(td, mp):
    """See 2010."""
    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {td.tmpdir} --style'
    tests.footnote_.run(cmd, mp=mp)

    style = decider_footnote.path.style(td.tmpdir)
    result = serializeraw.load_findings(style, 2010)

    result = [finding for finding in result if finding.location.page == 40]
    assert not result


@utilatest.requires(power.MASTER089_PDF)
def test_highnote_inside_master89_page45(td, mp):
    """Regression: Font size error on last footnote white space which is
    defined as following page number which differs in font size."""
    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {td.tmpdir} --style'
    tests.footnote_.run(cmd, mp=mp)

    style = decider_footnote.path.style(td.tmpdir)
    result = serializeraw.load_findings(style, 2010)

    result = [finding for finding in result if finding.location.page == 45]
    assert not result


@utilatest.requires(power.BACHELOR037_PDF)
def test_footnote_bachelor37page9(td, mp, capsys):
    cmd = f'-i {power.link(power.BACHELOR037_PDF)} -o {td.tmpdir} --style'
    tests.footnote_.run(cmd, mp=mp)
    assert 'ambiguous expected' not in utilatest.stderr(capsys)

    style = decider_footnote.path.style(td.tmpdir)
    result = serializeraw.load_findings(style, msgids=2005, pages=9)

    # do not detect invalid `Arial` error
    assert not result
