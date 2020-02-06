# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import border.cli
import tests.resources


@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.DOCU_TWINE_GENERATED, id='twine'),
    pytest.param(tests.resources.TECHNICAL24_GENERATED, id='technical24'),
    pytest.param(tests.resources.MASTER78_GENERATED, id='master78'),
])
@utila.skip_longrun
def test_border_cli_decider(source, testdir, monkeypatch):  # pylint:disable=W0621
    """Run `border` to extract common BoundingBox and check pages
    against this common box."""
    root = str(testdir)

    cmd = f'-i {source} -o {root} --pages=0:10'
    utila.run_command(
        cmd,
        process=border.cli.PROCESS,
        main=border.cli.main,
        monkeypatch=monkeypatch,
        success=True,
    )

    outputfile = f'{border.cli.PROCESS}__{border.cli.FEATURE_NAME}_hits.yaml'
    outputfile = os.path.join(root, outputfile)

    dumped = utila.file_read(outputfile)
    assert len(dumped) > 100  # result contains some content
