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

import decider_textflow.path
import tests.textflow_


def test_lineendings_master83_page6_lineending(testdir, monkeypatch):  # pylint:disable=W0621
    source = power.link(power.MASTER083_PDF)
    tests.textflow_.run_textflow(
        source,
        pages='6',
        lineending=True,
        quotation=True,
    )
    # lint result
    tests.textflow_.run(f'-i={source}', monkeypatch=monkeypatch)

    result = serializeraw.load_findings(
        decider_textflow.path.lineendings_linted(testdir.tmpdir),
        7000,
    )
    assert len(result) == 2, str(result)
