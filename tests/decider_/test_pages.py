# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import protocol
import serializeraw

import decider.features.page
import tests.resources


def user_work(path: str):
    headerfooter = iamraw.path.headerfooters(path)
    user, _ = decider.features.page.work(headerfooter)
    loaded = protocol.load_result(user)
    return loaded


def test_pages_work(monkeypatch):
    loader = serializeraw.load_headerfooter

    def scrumble_load(path: str, pages: tuple = None):
        loaded = loader(path, pages)
        loaded[4].footer.page.value = 10
        loaded[4].footer.page.raw = '10'
        return loaded

    with monkeypatch.context() as context:
        context.setattr(serializeraw, 'load_headerfooter', scrumble_load)
        result = user_work(tests.resources.TECHNICAL24)
    assert len(result) == 1, result
    assert result[0].solution.title
    assert result[0].solution.description
