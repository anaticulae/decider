# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import decider.example


@utilatest.nightly
def test_example_extract(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        power.DOCU035_PDF,
        power.TECH024_PDF,
    ]
    decider.example.extract(
        pdfs,
        generated,
        pages='0:3',
        full=True,
    )
    assert os.path.exists(generated), str(generated)
