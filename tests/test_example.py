# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import decider.example
import tests.resources


@utila.skip_longrun
def test_decider_example_extract(testdir):
    root = str(testdir)
    generated = os.path.join(root, 'generated')
    pdfs = [
        tests.resources.DOCU_TWINE,
        tests.resources.TECHNICAL24,
    ]
    decider.example.extract(pdfs, generated)

    assert os.path.exists(generated), str(generated)
