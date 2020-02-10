# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hey.path
import pytest
import serializeraw

import border.detection.leftright
import tests.resources


def load_example(path: str):
    # TODO: USE ONELINE?
    textpositions = serializeraw.load_textpositions(hey.path.textposition(path))
    pagesizes = serializeraw.load_pageborders(hey.path.sizeandborder(path))
    return textpositions, pagesizes


def load_leftright(path: str):
    textpositions, pagesizes = load_example(path)
    left, right = border.detection.leftright.determine_pageborder(
        textpositions,
        pagesizes,
    )
    return left, right


def test_leftright_run():
    """Detect book-like document with different border for left and
    right page."""
    left, right = load_leftright(tests.resources.LEFTRIGHT_GENERATED)
    result = border.detection.leftright.simple(left, right)
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result


def test_leftright_run_noleftright():
    """Ensure that document with single page layout has no different
    border for left and right but only a single border."""
    textpositions, pagesizes = load_example(tests.resources.MASTER72_GENERATED)
    result = border.detection.leftright.run(textpositions, pagesizes)
    assert result.valid is False, result
    # ensure that left border is more left then right
    assert result.left < result.right, result


@pytest.mark.xfail(reason='current approach is not strong enough')
def test_leftright_two_errorpages():
    """Introduce error to challenge algorithm."""
    textpositions, pagesizes = load_example(tests.resources.LEFTRIGHT_GENERATED)
    # introduce an error
    textpositions[1] = textpositions[0]
    pagesizes[1] = pagesizes[0]
    # introduce second error
    textpositions[4] = textpositions[5]
    pagesizes[4] = pagesizes[5]
    result = border.detection.leftright.run(textpositions, pagesizes)
    assert result.valid, result
    assert isinstance(result.left, tuple), result
    assert isinstance(result.right, tuple), result
