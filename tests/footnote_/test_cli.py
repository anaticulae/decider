# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import decider_footnote.path
import tests.footnote_
import tests.resources


def test_decider_footnote_cli_help(monkeypatch):
    tests.footnote_.run('--help', monkeypatch=monkeypatch)


def test_cli_rules(testdir, monkeypatch):  ## pylint:disable=W0621
    root = str(testdir)

    cmd = f'-i {tests.resources.MASTER72} -o {root} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    outpath = decider_footnote.path.rules(root)
    assert os.path.exists(outpath), outpath

    dumped = utila.file_read(outpath)
    assert len(dumped) > 1000  # result contains some content
    assert '{%number%}' not in dumped, dumped  # ensure that template is replaced


def test_cli_footnote_global(testdir, monkeypatch):  ## pylint:disable=W0621
    root = str(testdir)

    cmd = f'-i {tests.resources.BACHELOR90} -o {root} --global'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    global_ = decider_footnote.path.global_(root)
    result = tests.load_byid(global_, 2015)
    assert len(result) == 1
