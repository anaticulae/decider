# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw
import utilatest

import decider.features.page


def user_work(path: str):
    headerfooter = iamraw.path.headerfooters(path)
    user, _ = decider.features.page.work(headerfooter, sections=None)
    loaded = serializeraw.load_findings(user)
    return loaded


@utilatest.requires(power.TECH024_PDF)
def test_pages_work(mp):
    loader = serializeraw.load_headerfooter

    def scrumble_load(path: str, pages: tuple = None):
        loaded = loader(path, pages)
        loaded[4].footer.page.value = 10
        loaded[4].footer.page.raw = '10'
        return loaded

    with mp.context() as context:
        context.setattr(serializeraw, 'load_headerfooter', scrumble_load)
        result = user_work(power.link(power.TECH024_PDF))
    assert len(result) == 1, result
    assert result[0].solution.title
    assert result[0].solution.description
