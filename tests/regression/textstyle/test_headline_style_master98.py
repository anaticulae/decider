# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol

import decider_textstyle
import decider_textstyle.features.headlines
import tests.textstyle_


def test_headline_font_family_validation_page6(testdir, monkeypatch):
    """The headline text is formatted in Times New Roman. The whitespace
    between text and number is formatted in Arial. In normal mode, this
    is not a problem and we skip this. Therefore no linting must
    occur."""
    source = power.link(power.MASTER098_PDF)
    cmd = f'-i {source}  --headlines --pages=6'
    tests.textstyle_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    loaded = protocol.load_result(path, msgids={7501})
    assert not loaded

    with monkeypatch.context() as context:
        # run linter in ``expert`` mode
        context.setattr(
            decider_textstyle.features.headlines,
            'WHITESPACE_LINTING',
            True,
        )
        tests.textstyle_.run(cmd, monkeypatch=monkeypatch)
    loaded = protocol.load_result(path, msgids={7501})
    assert len(loaded) == 1
