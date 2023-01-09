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
def test_footnote_uppercase_start_master89_page40(td, mp):
    """Support quotation start char, see: 2001"""
    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)

    rules = decider_footnote.path.rules(td.tmpdir)
    result = serializeraw.load_findings(rules, 2001)

    result = [finding for finding in result if finding.location.page == 40]
    assert not result


@utilatest.requires(power.MASTER089_PDF)
def test_footnote_dot_end_master89_page46(td, mp):
    """Support quotation end char, see: 2002"""
    cmd = f'-i {power.link(power.MASTER089_PDF)} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)

    rules = decider_footnote.path.rules(td.tmpdir)
    result = serializeraw.load_findings(rules, 2002)

    result = [finding for finding in result if finding.location.page == 46]
    assert not result
