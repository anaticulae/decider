# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest
import serializeraw
import utila

import decider_footnote.path
import tests.footnote_

REGRESSION = """\
HOME018_PDF 16 !2019 # Ebd. follows Ebd. which is not a problem
MASTER155_PDF 16 !1337 # TODO REMOVE LATER
"""


def prepare(todo):
    for line in todo.strip().splitlines():
        content, message = line.split('#')
        source, pages, findings = content.split()
        pages = utila.parse_pages(pages)
        source = power.link(getattr(power, source))
        finding, nofinding = utila.partition(
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
def test_footnote_regression(source, pages, finding, nofinding, testdir,
                             monkeypatch):
    cmd = f'-i {source} -o {testdir.tmpdir} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(testdir.tmpdir)
    rules = serializeraw.load_findings(rules, pages=pages)

    finding_current = protocol.count_findings(rules, finding)
    nofinding_current = protocol.select_findings(rules, nofinding)
    assert finding_current == len(finding)
    assert not nofinding_current


def test_footnote_separator_distance(testdir, monkeypatch):
    cmd = f'-i {power.link(power.MASTER155_PDF)} -o {testdir.tmpdir} --rules'
    tests.footnote_.run(cmd, monkeypatch=monkeypatch)

    rules = decider_footnote.path.rules(testdir.tmpdir)
    rules = serializeraw.load_findings(rules)

    # TODO: DECREASE SEPARATOR_FOOTNOTE_DISTANCE_MAX to verify that
    # enable after upgrading protocol
    # -hv:separator_footnote_max_distance=0
    # linting works
    result = protocol.count_findings(rules, 2016)
    assert not result
