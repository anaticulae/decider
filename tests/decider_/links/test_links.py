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
import words.path

import decider.features.links


def test_links_work():
    linkpath = words.path.links(power.link(power.MASTER075_PDF))
    links = decider.features.links.work(linkpath)
    findings = serializeraw.load_findings(links[0])
    assert findings
