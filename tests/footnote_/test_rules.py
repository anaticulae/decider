# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import utilotest

import tests


@utilotest.requires(hoverpower.DISS480_PDF)
def test_footnote_incomplete_page(td, mp):
    """Footnote contains incomplete page number at the end.

    Diss480p5:
        2  T. Hoffmann, Das letzte Kommando – Ein Minister erinnert sich, Berlin, Bonn, Herford 1993, S.
    """
    source = hoverpower.link(hoverpower.DISS480_PDF)
    cmd = f'-i {source} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)
    rules = protoerror.findings_from_path(td.tmpdir, msgid=2100)
    assert len(rules) == 1


@utilotest.requires(hoverpower.MASTER193_PDF)
def test_footnote_missing_space(td, mp):
    """\
    243Vgl.: al-Mubarrad
    """
    source = hoverpower.link(hoverpower.MASTER193_PDF)
    cmd = f'-i {source} -o {td.tmpdir} --rules --pages=80:100'
    tests.footnote_.run(cmd, mp=mp)
    rules = protoerror.findings_from_path(td.tmpdir, msgid=2105)
    assert len(rules) == 5
