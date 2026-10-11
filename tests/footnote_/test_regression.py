# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import pytest
import serializeraw
import utilo
import utilotest

import decider_footnote.path
import tests.footnote_

REGRESSION = """\
HOME018_PDF 16 !2019 # Ebd. follows Ebd. which is not a problem
MASTER155_PDF 16 !1337 # TODO REMOVE LATER
BACHELOR077_PDF : !2100 #  Vgl. Dixon, S.: unvollstandige Seitenangabe
"""


def prepare(todo):
    for line in todo.strip().splitlines():
        content, message = line.split('#')
        source, pages, findings = content.split()
        pages = utilo.parse_pages(pages)
        source = hoverpower.link(getattr(hoverpower, source))
        finding, nofinding = utilo.partition(
            lambda x: x[0] != '!',
            findings.split(),
        )
        finding = [int(item) for item in finding]
        nofinding = set(int(item[1:]) for item in nofinding)
        message = message.replace(' ', '')
        yield pytest.param(source, pages, finding, nofinding, id=message)


@pytest.mark.parametrize(
    'source, pages, finding, nofinding',
    list(prepare(REGRESSION)),
)
def test_footnote_regression(source, pages, finding, nofinding, td, mp):
    utilotest.fixture_requires(source)
    cmd = f'-i {source} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)

    rules = decider_footnote.path.rules(td.tmpdir)
    rules = serializeraw.load_findings(rules, pages=pages)

    finding_current = protoerror.count_findings(rules, finding)
    nofinding_current = protoerror.select_findings(rules, nofinding)
    assert finding_current == len(finding)
    assert not nofinding_current


@utilotest.requires(hoverpower.MASTER155_PDF)
def test_footnote_separator_distance(td, mp):
    cmd = f'-i {hoverpower.link(hoverpower.MASTER155_PDF)} -o {td.tmpdir} --rules'
    tests.footnote_.run(cmd, mp=mp)

    rules = decider_footnote.path.rules(td.tmpdir)
    rules = serializeraw.load_findings(rules)

    # TODO: DECREASE SEPARATOR_FOOTNOTE_DISTANCE_MAX to verify that
    # enable after upgrading protoerror
    # -hv:separator_footnote_max_distance=0
    # linting works
    result = protoerror.count_findings(rules, 2016)
    assert not result
