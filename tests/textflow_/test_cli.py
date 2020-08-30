# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila

import tests.textflow_


def test_decider_textflow_cli_help(monkeypatch):
    tests.textflow_.run('--help', monkeypatch=monkeypatch)


@pytest.mark.parametrize('source', [
    pytest.param(power.link(power.TECHNICAL_024), id='technical24'),
    pytest.param(power.link(power.BACHELOR037_PDF), id='bachelor37'),
    pytest.param(power.link(power.BACHELOR076_PDF), id='bachelor76'),
    pytest.param(power.link(power.DOCU35_PDF), id='docu'),
    pytest.param(power.link(power.BOOK007_PDF), id='leftright'),
    pytest.param(power.link(power.MASTER072_PDF), id='master72'),
    pytest.param(power.link(power.MASTER078_PDF), id='master78'),
    pytest.param(power.link(power.MASTER098_PDF), id='master98'),
    pytest.param(power.link(power.MASTER099_PDF), id='master99'),
])
def test_cli_textflow_example(source, testdir, monkeypatch):
    """Run textflow"""
    # TODO: MOVE TO TEST DATA GENERATOR
    utila.run(f'textflow -i {source}')
    cmd = f'-i {source}'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
