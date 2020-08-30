# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import decider_toc.duplicated


def test_duplicated_words():
    source = power.link(power.MASTER098_PDF)
    toc = serializeraw.load_toc(source)
    assert toc
    validated = decider_toc.duplicated.validate(toc)
    assert len(validated) == 2
