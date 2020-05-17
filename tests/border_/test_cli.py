# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import iamraw
import protocol
import pytest
import serializeraw
import utila

import border.cli
import border.features.detection
import border.path
import tests.resources


def validate_leftright(hits):
    expected_hits = []
    # text at bottom and
    expected_hits.append(0)
    # symbol at right top
    # TODO: reduce after extracting symbol as one
    expected_hits.extend([0] * 16)

    hits = utila.flatten(item.hits for item in hits)
    assert len(hits) >= len(expected_hits), (
        f'expected hits: {expected_hits}\n current: {len(hits)}\n')


def run_border_detector(
        root: str,
        source: str,
        monkeypatch,
) -> iamraw.PageContentHits:
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
    detected_hits = serializeraw.load_hits(dumped)
    return detected_hits


@pytest.mark.parametrize('source', [
    pytest.param(tests.resources.TECHNICAL24, id='technical24'),
])
def test_border_cli_decider_simple(source, testdir, monkeypatch):
    root = testdir.tmpdir
    detected = run_border_detector(root, source, monkeypatch)
    assert detected
    loaded = protocol.load_result(border.path.border_user(testdir.tmpdir))
    assert loaded


@pytest.mark.parametrize('source, validate', [
    pytest.param(tests.resources.DOCU_TWINE, [4, 4], id='twine'),
    pytest.param(tests.resources.MASTER78, [6, 8], id='master78'),
])
@utila.skip_longrun
def test_border_cli_decider_list(
        source,
        validate,
        testdir,
        monkeypatch,
):  # pylint:disable=W0621
    """Run `border` to extract common BoundingBox and check pages
    against this common box."""
    with patch_zero_border_tolerance(monkeypatch):
        detected_hits = run_border_detector(testdir.tmpdir, source, monkeypatch)
    assert detected_hits
    # validated
    assert len(detected_hits) >= len(validate), (
        f'expected hits: {validate}\ncurrent: {len(detected_hits)}\n'
        f'hits: {detected_hits}')
    loaded = protocol.load_result(border.path.border_user(testdir.tmpdir))
    assert loaded


@pytest.mark.parametrize('source, validate', [
    pytest.param(
        tests.resources.LEFTRIGHT,
        validate_leftright,
        id='leftright',
    ),
])
@utila.skip_longrun
def test_border_cli_decider_complex_validation(
        source,
        validate,
        testdir,
        monkeypatch,
):  # pylint:disable=W0621
    """Ensure to run border detection and load linter result later."""
    root = testdir.tmpdir
    with patch_zero_border_tolerance(monkeypatch):
        detected = run_border_detector(root, source, monkeypatch)
    validate(detected)
    loaded = protocol.load_result(border.path.border_user(testdir.tmpdir))
    assert loaded


@contextlib.contextmanager
def patch_zero_border_tolerance(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(border.features.detection, 'BORDER_LEFT', 0)
        context.setattr(border.features.detection, 'BORDER_RIGHT', 0)
        context.setattr(border.features.detection, 'BORDER_TOP', 0)
        context.setattr(border.features.detection, 'BORDER_BOTTOM', 0)
        yield
