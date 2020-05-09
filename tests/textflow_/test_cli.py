# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila

import tests.resources
import tests.textflow_


def test_decider_textflow_cli_help(monkeypatch):
    tests.textflow_.run('--help', monkeypatch=monkeypatch)


# yapf:disable
@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.TECHNICAL24_GENERATED, id='technical24'),
    pytest.param(tests.resources.BACHELOR37_GENERATED, id='bachelor37'),
    pytest.param(tests.resources.BACHELOR76_GENERATED, id='bachelor76'),
    pytest.param(tests.resources.DOCU_TWINE_GENERATED, id='docu'),
    pytest.param(tests.resources.LEFTRIGHT_GENERATED, id='leftright'),
    pytest.param(tests.resources.MASTER72_GENERATED, id='master72'),
    pytest.param(tests.resources.MASTER78_GENERATED, id='master78'),
    pytest.param(tests.resources.MASTER98_GENERATED, id='master98'),
    pytest.param(tests.resources.MASTER99_GENERATED, id='master99'),
])
# yapf:enable
def test_cli_textflow_example(source, testdir, monkeypatch):
    """Run textflow"""
    # TODO: MOVE TO TEST DATA GENERATOR
    utila.run(f'textflow -i {source}')
    cmd = f'-i {source}'
    tests.textflow_.run(cmd, monkeypatch=monkeypatch)
