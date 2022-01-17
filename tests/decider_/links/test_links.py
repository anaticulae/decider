# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import words.path

import decider
import decider.features.links
import tests


def test_links_work():
    linkpath = words.path.links(power.link(power.MASTER075_PDF))
    links = decider.features.links.work(linkpath)
    findings = serializeraw.load_findings(links[0])
    assert findings


def run_links(source, testdir, monkeypatch, online: bool = False, msgids=None):
    linkpath = power.link(source)
    # disable connecting to www
    monkeypatch.setenv(decider.DECIDER_ONELINE_FLAG, str(online))
    tests.run_decider(f'-i {linkpath} --links', monkeypatch)
    findings = serializeraw.load_findings(
        os.path.join(testdir.tmpdir, 'decider__links_user.yaml'),
        msgids=msgids,
    )
    return findings


@pytest.mark.parametrize('online', [True, False])
def test_links_validate(testdir, monkeypatch, online):
    findings = run_links(
        power.MASTER075_PDF,
        testdir,
        monkeypatch,
        online=online,
        msgids=10510,
    )
    assert findings if online else not findings


def test_links_date_mixed(testdir, monkeypatch):
    findings = run_links(
        power.MASTER098_PDF,
        testdir,
        monkeypatch,
        msgids=10520,
    )
    assert not findings


def test_links_single_access_date_mixed(testdir, monkeypatch):
    findings = run_links(
        power.MASTER098_PDF,
        testdir,
        monkeypatch,
        msgids=10521,
    )
    assert not findings  # TODO: CHANGE AFTER PARSING ALL DOCUMENT LINKS
