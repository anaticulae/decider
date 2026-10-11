# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import utilotest

import decider.example


@utilotest.nightly
def test_example_extract(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        hoverpower.DOCU035_PDF,
        hoverpower.TECH024_PDF,
    ]
    decider.example.extract(
        pdfs,
        generated,
        pages='0:3',
        full=True,
    )
    assert os.path.exists(generated), str(generated)
