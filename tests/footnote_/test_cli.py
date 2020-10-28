# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import serializeraw
import utila

import decider_footnote.path
import tests.footnote_


def test_decider_footnote_cli_help(monkeypatch):
    tests.footnote_.run('--help', monkeypatch=monkeypatch)


def test_cli_rules(testdir, monkeypatch):  # pylint:disable=W0621
    root = str(testdir)

    cmd = f'-i {power.link(power.MASTER072_PDF)} -o {root} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    outpath = decider_footnote.path.rules(root)
    assert os.path.exists(outpath), outpath

    dumped = utila.file_read(outpath)

    findings = serializeraw.load_findings(dumped)

    assert len(findings) >= 2  # result contains some findings

    # ensure that template is replaced
    assert utila.istemplate_replaced(dumped), dumped


def test_cli_footnote_global(testdir, monkeypatch):  # pylint:disable=W0621
    root = str(testdir)

    cmd = f'-i {power.link(power.BACHELOR090_PDF)} -o {root} --global'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    global_ = decider_footnote.path.global_(root)
    # TODO: REPLACE AFTER UPGRADING TO NEW PROTOCOL
    result = serializeraw.load_findings(global_, 2015)
    assert len(result) == 1


def test_cli_footnote_disabled_checker(testdir, monkeypatch):  # pylint:disable=W0621
    root = str(testdir)

    cmd = f'-i {power.link(power.BACHELOR076_PDF)} -o {root} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(root)

    # ensure that checker is disabled
    result = serializeraw.load_findings(rules, 2001)
    assert not result
    result = serializeraw.load_findings(rules, 2002)
    assert not result

    # ensure that info message was send
    result = serializeraw.load_findings(rules, 2013)
    assert len(result) == 1
    result = serializeraw.load_findings(rules, 2012)
    assert len(result) == 1
