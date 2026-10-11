# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import utilotest

import tests.decider_


@utilotest.requires(hoverpower.BACHELOR051_PDF)
def test_color_bachelor051(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR051_PDF)
    cmd = f'-i {source} --color --pages=20'
    tests.decider_.run(cmd, mp=mp)
    findings = protoerror.findings_from_path(td.tmpdir, msgid=10600)
    assert findings[0].page == 20
    findings = findings[0].content
    assert len(findings) == 4
