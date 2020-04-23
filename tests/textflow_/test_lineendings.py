# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import yaml

import decider_textflow.path
import tests.resources
import tests.textflow_


def run_textflow(
        source,
        pages,
        lineending: bool = False,
        quotation: bool = False,
):
    actions = ''
    if lineending:
        actions += ' --lineending'
    if quotation:
        actions += ' --quotation'
    utila.run(f'textflow -i {source} --pages={pages} {actions}')


def test_lineendings_master83_page6(testdir, monkeypatch):  # pylint:disable=W0621
    root = testdir.tmpdir
    run_textflow(
        tests.resources.MASTER83_GENERATED,
        pages='6',
        lineending=True,
        quotation=True,
    )

    # lint result
    tests.textflow_.run('', monkeypatch=monkeypatch)

    linted = decider_textflow.path.lineendings_linted(root)
    linted = load_linted(linted)
    assert len(linted) == 2, str(linted)


def load_linted(path: str):
    loaded = yaml.load(utila.file_read(path), Loader=yaml.FullLoader)
    return messageids(loaded)


def messageids(items):
    result = [item.msgid for item in items]
    return result
