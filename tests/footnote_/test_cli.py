# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import protocol
import pytest
import serializeraw
import utila
import utilatest

import decider_footnote.path
import tests.footnote_


def test_decider_footnote_cli_help(mp):
    tests.footnote_.run('--help', mp=mp)


@pytest.mark.xfail(reason='software integration')
@utilatest.requires(power.MASTER072_PDF)
def test_cli_rules(td, mp):
    source = power.link(power.MASTER072_PDF)
    cmd = f'-i {source} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)
    outpath = decider_footnote.path.rules(td.tmpdir)
    assert os.path.exists(outpath), outpath
    dumped = utila.file_read(outpath)
    findings = serializeraw.load_findings(dumped)
    assert len(findings) >= 2  # result contains some findings
    # ensure that template is replaced
    assert utila.istemplate_replaced(dumped), dumped


@pytest.mark.xfail(reason='software integration')
@utilatest.requires(power.BACHELOR090_PDF)
def test_cli_footnote_global(td, mp):
    cmd = f'-i {power.link(power.BACHELOR090_PDF)} -o {td.tmpdir} --global'
    tests.footnote_.run(cmd, mp=mp)
    findings = serializeraw.findings_from_path(td.tmpdir, msgid=2015)
    assert len(findings) == 1


@pytest.mark.xfail(reason='software integration')
@utilatest.requires(power.BACHELOR076_PDF)
def test_cli_footnote_disabled_checker(td, mp):
    cmd = f'-i {power.link(power.BACHELOR076_PDF)} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)

    rules = decider_footnote.path.rules(td.tmpdir)
    rules = serializeraw.load_findings(rules)

    result = protocol.count_findings(rules, 2001)
    assert result == 1
    # ensure that checker is disabled
    result = protocol.count_findings(rules, 2002)
    assert not result

    # ensure that info message was send
    result = protocol.count_findings(rules, 2013)
    assert result == 1
    result = protocol.count_findings(rules, 2012)
    assert not result
