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


def run_paragraph_length_linter(source, pages, testdir, monkeypatch):
    # TODO: REPLACE WITH UTILA CODE
    pages = ','.join([str(item) for item in pages])
    cmd = f'-i={source} --paragraph --pages={pages}'

    tests.textflow_.run(cmd, monkeypatch=monkeypatch)

    result = tests.load_byid(
        decider_textflow.path.paragraph_linted(testdir.tmpdir),
        7630,
    )
    return result


def test_paragraph_too_short(testdir, monkeypatch):
    source = tests.resources.BACHELOR90
    pages = (12, 13, 14)
    result = run_paragraph_length_linter(source, pages, testdir, monkeypatch)
    assert len(result) == 7, str(result)


def test_list_no_paragraph_too_short(testdir, monkeypatch):
    source = tests.resources.MASTER72
    pages = (7,)
    result = run_paragraph_length_linter(source, pages, testdir, monkeypatch)
    result = [item for item in result if item.location.page == 7]
    # TODO: This content before a list should not be an error
    # REMAINING ERROR:
    # O’Reilly nennt in seinem Artikel sieben Hauptpunkte, die das Web 2.0
    # kennzeichnen10:
    assert len(result) == 1, str(result)
