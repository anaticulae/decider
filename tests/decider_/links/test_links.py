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
import utilatest
import weblink.path

import decider
import decider.features.links
import tests


@utilatest.requires(power.MASTER075_PDF)
def test_links_work():
    source = power.link(power.MASTER075_PDF)
    linkpath = weblink.path.weblink_sentence(source)
    links = decider.features.links.work(
        biblio=None,
        footer=None,
        sentence=linkpath,
    )
    findings = serializeraw.load_findings(links[0])
    assert findings


def run_links(source, td, mp, online: bool = False, msgids=None):
    utilatest.fixture_requires(source)
    linkpath = power.link(source)
    # disable connecting to www
    mp.setenv(decider.DECIDER_ONELINE_FLAG, str(online))
    tests.run(f'-i {linkpath} --links', mp=mp)
    findings = serializeraw.load_findings(
        os.path.join(td.tmpdir, 'decider__links_user.yaml'),
        msgids=msgids,
    )
    return findings


@pytest.mark.parametrize('online', [True, False])
def test_links_validate(td, mp, online):
    findings = run_links(
        power.MASTER075_PDF,
        td,
        mp,
        online=online,
        msgids=10510,
    )
    assert findings if online else not findings


def test_links_date_mixed(td, mp):
    findings = run_links(
        power.MASTER098_PDF,
        td,
        mp,
        msgids=10520,
    )
    assert not findings


def test_links_single_access_date_mixed(td, mp):
    findings = run_links(
        power.MASTER098_PDF,
        td,
        mp,
        msgids=10521,
    )
    assert not findings  # TODO: CHANGE AFTER PARSING ALL DOCUMENT LINKS


def test_local_link_bachelor028(td, mp):
    findings = run_links(
        power.BACHELOR028_PDF,
        td,
        mp,
        msgids=10515,
    )
    # if not works, verify hyperlink file:/// parser
    assert len(findings) == 2
