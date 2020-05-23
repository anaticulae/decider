# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

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
        tests.resources.MASTER83,
        pages='6',
        lineending=True,
        quotation=True,
    )

    # lint result
    tests.textflow_.run('', monkeypatch=monkeypatch)

    loaded = [item.content for item in protocol.findings_from_path(root)]
    loaded = utila.flatten(loaded)
    linted = [item.msgid for item in loaded]
    assert len(linted) == 2, str(linted)
