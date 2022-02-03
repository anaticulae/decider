# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol

import tests


def test_footnote_incomplete_page(testdir, monkeypatch):
    """Footnote contains incomplete page number at the end.

    Diss480p5:
        2  T. Hoffmann, Das letzte Kommando – Ein Minister erinnert sich, Berlin, Bonn, Herford 1993, S.
    """
    source = power.link(power.DISS480_PDF)
    cmd = f'-i {source} -o {testdir.tmpdir} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)
    rules = protocol.findings_from_path(testdir.tmpdir, msgid=2100)
    assert len(rules) == 1
