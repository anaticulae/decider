# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import decider_textflow.path
import tests
import tests.resources
import tests.textflow_


def test_paragraph_too_short(testdir, monkeypatch):  # pylint:disable=W0621
    source = tests.resources.BACHELOR90
    cmd = f'-i={source} --paragraph --pages=12,13,14'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = tests.load_byid(
        decider_textflow.path.paragraph_linted(testdir.tmpdir),
        7630,
    )
    assert len(result) == 7, str(result)
