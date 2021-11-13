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

import decider_textflow.path
import tests.textflow_


def test_lineendings_master83page6_lineending(testdir, monkeypatch):
    source = power.link(power.MASTER083_PDF)
    tests.textflow_.run_textflow(
        source,
        pages=6,
        lineending=True,
        quotation=True,
    )
    # lint result
    tests.textflow_.run(f'-i={source} --pages=6', monkeypatch=monkeypatch)
    result = serializeraw.load_findings(
        decider_textflow.path.lineendings_linted(testdir.tmpdir),
        7000,
    )
    assert len(result) == 2, str(result)


def test_list_not_included_bachelor67page10(testdir, monkeypatch):
    source = power.link(power.BACHELOR067_PDF)
    # lint result
    cmd = f'-i={source} --pages=10 --lineending'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    result = serializeraw.findings_from_path(testdir.tmpdir, msgid=7005)
    assert len(result) == 1, str(result)


def test_list_better_included_bachelor67page10(testdir, monkeypatch):
    source = power.link(power.BACHELOR067_PDF)
    # lint result
    cmd = f'-i={source} --pages=10 --lineending'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    result = serializeraw.findings_from_path(testdir.tmpdir, msgid=7006)
    assert len(result) == 1, str(result)


def test_formula_better_included_home050page31(testdir, monkeypatch):
    source = power.link(power.HOME050_PDF)
    cmd = f'-i={source} -o {testdir.tmpdir} --pages=31 --lineending'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
    result = serializeraw.findings_from_path(testdir.tmpdir, msgid=7011)
    assert len(result) == 1, str(result)
