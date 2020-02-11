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
import serializeraw
import utila

import border.cli
import tests.resources


def validate_leftright(hits):
    expected_hits = []
    # text at bottom and
    expected_hits.append(0)
    # symbol at right top
    # TODO: reduce after extracting symbol as one
    expected_hits.extend([0] * 16)
    assert len(hits) >= len(expected_hits), (
        f'expected hits: {expected_hits}\n current: {len(hits)}\n')


@pytest.mark.parametrize('source, validate', [
    pytest.param(tests.resources.DOCU_TWINE_GENERATED, [4, 4], id='twine'),
    pytest.param(tests.resources.TECHNICAL24_GENERATED, None, id='technical24'),
    pytest.param(tests.resources.MASTER78_GENERATED, [6, 8], id='master78'),
    pytest.param(
        tests.resources.LEFTRIGHT_GENERATED,
        validate_leftright,
        id='leftright',
    ),
])
@utila.skip_longrun
def test_border_cli_decider(
        source,
        validate,
        testdir,
        monkeypatch,
):  # pylint:disable=W0621
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
    detected_border, detected_hits = serializeraw.load_hits(outputfile)

    if validate is None:
        return
    if isinstance(validate, list):
        # validated
        assert len(detected_hits) >= len(validate), (
            f'expected hits: {validate}\ncurrent: {len(detected_hits)}\n'
            f'border: {detected_border}\nhits: {detected_hits}')
        return
    validate(detected_hits)
